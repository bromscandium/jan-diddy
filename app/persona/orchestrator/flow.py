import random
import time

from telegram.ext import CallbackContext

from app.core.bot import bot_settings
from app.core.llm import trigger_config
from app.core.logger import logger
from app.persona import client, history, profiles, scoring, state, triggers
from app.persona.orchestrator.addressing import is_addressed
from app.persona.orchestrator.formatting import context_text, format_outgoing
from app.persona.orchestrator.ingest import ingest
from app.persona.orchestrator.payload import build_payload
from app.utils.typing import type_then_send


async def _score_previous(chat_id: int, thread_id: int | None, msg) -> None:
    last_bot = await scoring.last_bot_message(chat_id, thread_id)
    if last_bot is None:
        return
    replied = bool(msg.reply_to_message and msg.reply_to_message.message_id == last_bot)
    if replied or scoring.has_signal(msg.text):
        await scoring.apply_reply_signal(chat_id, last_bot, msg.text)


async def _reply(update, context: CallbackContext, msg, current_text: str, user_id, username: str, ts: int) -> None:
    chat_id = msg.chat_id
    thread_id = msg.message_thread_id
    reply_to_id = msg.reply_to_message.message_id if msg.reply_to_message else None

    if bot_settings.REPLY_MODE == "off":
        logger.debug("skip: REPLY_MODE=off")
        return

    cfg = trigger_config()
    last_bot = await scoring.last_bot_message(chat_id, thread_id)
    addressed = await is_addressed(msg, context, last_bot)

    if bot_settings.REPLY_MODE == "addressed" and not addressed:
        logger.debug("skip: REPLY_MODE=addressed and not addressed")
        return

    track = "addr" if addressed else "spont"
    track_cfg = cfg.addressed if addressed else cfg.spontaneous

    spont_state = await state.get_track(chat_id, thread_id, "spont")
    if triggers.should_prewarm(spont_state, cfg):
        await client.prewarm()
        await state.mark_prewarmed(chat_id, thread_id)

    track_state = spont_state if track == "spont" else await state.get_track(chat_id, thread_id, "addr")
    bias = await profiles.bias(user_id)
    if not triggers.should_reply(track_cfg, track_state, cfg, bias):
        logger.debug(
            f"skip [{track}] addressed={addressed} count={track_state['count']}/{track_cfg.min_messages} "
            f"prob={track_cfg.probability}*bias={bias:.2f}"
        )
        return

    ctx = await state.get_context(chat_id, thread_id)
    payload = build_payload(ctx, reply_to_id, msg, ts)
    target = {"user_id": user_id, "username": username, "text": current_text} if addressed else None
    mode = "addressed" if addressed else "spontaneous"
    reply = await client.generate(payload, chat_id, thread_id, mode=mode, target=target)
    logger.debug(
        f"[{mode}] target={(target or {}).get('text')!r} ctx({len(payload)}):\n  "
        + "\n  ".join(f"{m['username']}: {m['text']}" for m in payload)
        + f"\n  => {reply!r}"
    )
    if not reply:
        return

    norm = reply.strip().casefold()
    if norm in await state.recent_replies(chat_id, thread_id):
        logger.debug(f"skip duplicate reply {reply!r}")
        return
    await state.remember_reply(chat_id, thread_id, norm)

    if addressed:
        reply_to = msg.message_id
    else:
        reply_to = ctx[-1]["message_id"] if ctx and random.random() < cfg.reply_probability else None
    sent = await type_then_send(
        context.bot, chat_id, format_outgoing(reply), message_thread_id=thread_id, reply_to_message_id=reply_to
    )
    await state.register_reply(chat_id, thread_id, track, time.time(), track_cfg.cooldown_minutes)
    await profiles.mark_replied(user_id, username)
    ctx_text = context_text(ctx)
    await history.save_bot_reply(chat_id, thread_id, sent.message_id if sent else None, ctx_text, reply)
    if sent:
        await scoring.register_pending(
            chat_id, thread_id, sent.message_id, ctx_text, reply,
            user_id if addressed else None, username if addressed else "",
        )


async def handle_text(update, context: CallbackContext, msg) -> None:
    reply_to_id = msg.reply_to_message.message_id if msg.reply_to_message else None
    user_id, username, ts = await ingest(msg, msg.text, reply_to_id)
    await _score_previous(msg.chat_id, msg.message_thread_id, msg)
    await scoring.sweep_ignored(msg.chat_id, msg.message_thread_id, ts)
    await _reply(update, context, msg, msg.text, user_id, username, ts)


async def handle_media(update, context: CallbackContext, msg, text: str) -> None:
    reply_to_id = msg.reply_to_message.message_id if msg.reply_to_message else None
    user_id, username, ts = await ingest(msg, text, reply_to_id)
    await _reply(update, context, msg, text, user_id, username, ts)
