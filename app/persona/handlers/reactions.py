from telegram import Update
from telegram.ext import CallbackContext

from app.persona.services import scoring


async def on_reaction(update: Update, context: CallbackContext) -> None:
    mr = update.message_reaction
    if not mr or not mr.new_reaction:
        return
    reaction = mr.new_reaction[-1]
    emoji = getattr(reaction, "emoji", None)
    if not emoji:
        return
    await scoring.apply_reaction(mr.chat.id, mr.message_id, emoji)
