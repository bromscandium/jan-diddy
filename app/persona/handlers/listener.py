import random
import time

from telegram import Update
from telegram.ext import CallbackContext

from app.core.llm import trigger_config
from app.persona.services import history, persona_client, profiles, scoring, state, triggers
from app.utils.typing import type_then_send


def _context_text(ctx: list[dict]) -> str:
    return "\n".join(f"{m['username']}: {m['text']}" for m in ctx)


async def _is_addressed(msg, context: CallbackContext, last_bot: int | None) -> bool:
    if msg.reply_to_message:
        replied = msg.reply_to_message
        if last_bot is not None and replied.message_id == last_bot:
            return True
        if replied.from_user and replied.from_user.id == context.bot.id:
            return True
    handle = f"@{context.bot.username}"
    for ent in msg.entities or []:
        if ent.type == "mention" and msg.text[ent.offset:ent.offset + ent.length] == handle:
            return True
        if ent.type == "text_mention" and ent.user and ent.user.id == context.bot.id:
            return True
    return False


async def _score_previous(chat_id: int, thread_id: int | None, msg) -> None:
    last_bot = await scoring.last_bot_message(chat_id, thread_id)
    if last_bot is None:
        return
    replied = bool(msg.reply_to_message and msg.reply_to_message.message_id == last_bot)
    if replied or scoring.has_signal(msg.text):
        await scoring.apply_reply_signal(chat_id, last_bot, msg.text)


async def listener(update: Update, context: CallbackContext) -> None:
    msg = update.effective_message
    if not msg or not msg.text:
        return
    user = msg.from_user
    if user and user.is_bot:
        return

    chat_id = msg.chat_id
    thread_id = msg.message_thread_id
    user_id = user.id if user else None
    username = user.full_name if user else "anon"
    ts = int(msg.date.timestamp()) if msg.date else int(time.time())

    await state.record_incoming(chat_id, thread_id, user_id, username, msg.text, msg.message_id, ts)
    await history.save_message(chat_id, thread_id, msg.message_id, user_id, username, msg.text, ts)
    await _score_previous(chat_id, thread_id, msg)

    cfg = trigger_config()
    last_bot = await scoring.last_bot_message(chat_id, thread_id)
    addressed = await _is_addressed(msg, context, last_bot)
    track = "addr" if addressed else "spont"
    track_cfg = cfg.addressed if addressed else cfg.spontaneous

    spont_state = await state.get_track(chat_id, thread_id, "spont")
    if triggers.should_prewarm(spont_state, cfg):
        await persona_client.prewarm()
        await state.mark_prewarmed(chat_id, thread_id)

    track_state = spont_state if track == "spont" else await state.get_track(chat_id, thread_id, "addr")
    bias = await profiles.bias(user_id)
    if not triggers.should_reply(track_cfg, track_state, cfg, bias):
        return

    ctx = await state.get_context(chat_id, thread_id)
    payload = [{"username": m["username"], "text": m["text"]} for m in ctx]
    target = {"user_id": user_id, "username": username, "text": msg.text} if addressed else None
    reply = await persona_client.generate(payload, chat_id, thread_id, mode=track, target=target)
    if not reply:
        return

    if addressed:
        reply_to = msg.message_id
    else:
        reply_to = ctx[-1]["message_id"] if ctx and random.random() < cfg.reply_probability else None
    sent = await type_then_send(
        context.bot, chat_id, reply, message_thread_id=thread_id, reply_to_message_id=reply_to
    )
    await state.register_reply(chat_id, thread_id, track, time.time(), track_cfg.cooldown_minutes)
    context_text = _context_text(ctx)
    await history.save_bot_reply(chat_id, thread_id, sent.message_id if sent else None, context_text, reply)
    if sent:
        await scoring.register_pending(
            chat_id, thread_id, sent.message_id, context_text, reply, user_id, username
        )
