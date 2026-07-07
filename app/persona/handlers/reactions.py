from telegram import Update
from telegram.ext import CallbackContext

from app.persona.services import scoring


async def on_reaction(update: Update, context: CallbackContext) -> None:
    mr = update.message_reaction
    if not mr or not mr.new_reaction:
        return
    await scoring.mark_success(mr.chat.id, mr.message_id, weight=2)
