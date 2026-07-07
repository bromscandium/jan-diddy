import random
import time

from telegram import Update
from telegram.ext import CallbackContext

from app.core.llm import trigger_config
from app.persona.services import history, persona_client, scoring, state, triggers
from app.utils.typing import type_then_send


def _context_text(ctx: list[dict]) -> str:
    return "\n".join(f"{m['username']}: {m['text']}" for m in ctx)


async def _check_success(chat_id: int, thread_id: int | None, msg) -> None:
    last_bot = await scoring.last_bot_message(chat_id, thread_id)
    if last_bot is None:
        return
    replied = bool(msg.reply_to_message and msg.reply_to_message.message_id == last_bot)
    if replied or scoring.contains_success_keyword(msg.text):
        await scoring.mark_success(chat_id, last_bot)


async def listener(update: Update, context: CallbackContext) -> None:
    msg = update.effective_message
    if not msg or not msg.text:
        return
    user = msg.from_user
    if user and user.is_bot:
        return

    chat_id = msg.chat_id
    thread_id = msg.message_thread_id
    username = user.full_name if user else "anon"
    ts = int(msg.date.timestamp()) if msg.date else int(time.time())

    await state.record_incoming(chat_id, thread_id, username, msg.text, msg.message_id, ts)
    await history.save_message(
        chat_id, thread_id, msg.message_id, user.id if user else None, username, msg.text, ts
    )
    await _check_success(chat_id, thread_id, msg)

    cfg = trigger_config()
    st = await state.get_state(chat_id, thread_id)

    if triggers.should_prewarm(st, cfg):
        await persona_client.prewarm()
        await state.mark_prewarmed(chat_id, thread_id)

    if not triggers.should_reply(st, cfg):
        return

    ctx = await state.get_context(chat_id, thread_id)
    payload = [{"username": m["username"], "text": m["text"]} for m in ctx]
    reply = await persona_client.generate(payload, chat_id, thread_id)
    if not reply:
        return

    reply_to = ctx[-1]["message_id"] if ctx and random.random() < cfg.reply_probability else None
    sent = await type_then_send(
        context.bot,
        chat_id,
        reply,
        message_thread_id=thread_id,
        reply_to_message_id=reply_to,
    )
    await state.register_reply(chat_id, thread_id, time.time(), cfg.cooldown_minutes)
    context_text = _context_text(ctx)
    await history.save_bot_reply(
        chat_id, thread_id, sent.message_id if sent else None, context_text, reply
    )
    if sent:
        await scoring.register_pending(chat_id, thread_id, sent.message_id, context_text, reply)
