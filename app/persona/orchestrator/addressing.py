from telegram.ext import CallbackContext


async def is_addressed(msg, context: CallbackContext, last_bot: int | None) -> bool:
    if msg.reply_to_message:
        replied = msg.reply_to_message
        if last_bot is not None and replied.message_id == last_bot:
            return True
        if replied.from_user and replied.from_user.id == context.bot.id:
            return True
    text = msg.text or msg.caption or ""
    handle = f"@{context.bot.username}"
    for ent in msg.entities or msg.caption_entities or []:
        if ent.type == "mention" and text[ent.offset:ent.offset + ent.length] == handle:
            return True
        if ent.type == "text_mention" and ent.user and ent.user.id == context.bot.id:
            return True
    return False
