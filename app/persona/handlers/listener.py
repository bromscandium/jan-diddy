from telegram import Update
from telegram.ext import CallbackContext

from app.core.llm import llm_settings
from app.persona import orchestrator


async def listener(update: Update, context: CallbackContext) -> None:
    msg = update.effective_message
    if not msg or not msg.text or not orchestrator.in_persona_thread(msg):
        return
    await orchestrator.handle_text(update, context, msg)


async def media_listener(update: Update, context: CallbackContext) -> None:
    if llm_settings.PERSONA_FORMAT != "tagged":
        return
    msg = update.effective_message
    if not orchestrator.in_persona_thread(msg):
        return
    text = await orchestrator.media_text(msg, context.bot)
    if not text:
        return
    await orchestrator.ingest(msg, text)
