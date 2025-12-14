from datetime import datetime
from telegram import Update
from app.core.config import bot_settings
from app.utils.decorators import usage_limit


@usage_limit
async def rules(update: Update, context):
    await update.message.reply_text(
        'čítali ste kanál <a href="https://t.me/c/2307996875/4/224676">ASAP</a>?',
        parse_mode="HTML"
    )


@usage_limit
async def moodle(update: Update, context):
    await context.bot.forward_message(
        chat_id=update.effective_chat.id,
        from_chat_id=bot_settings.chat_id,
        message_id=224679,
        message_thread_id=update.message.message_thread_id,
    )


@usage_limit
async def links(update: Update, context):
    await context.bot.forward_message(
        chat_id=update.effective_chat.id,
        from_chat_id=bot_settings.chat_id,
        message_id=224678,
        message_thread_id=update.message.message_thread_id,
    )


@usage_limit
async def scores(update: Update, context):
    await update.message.reply_text(
        'Čítali ste kanál <a href="https://t.me/c/2307996875/4/224680">ASAP</a>?',
        parse_mode="HTML"
    )


@usage_limit
async def plan(update: Update, context):
    await context.bot.forward_message(
        chat_id=update.effective_chat.id,
        from_chat_id=bot_settings.chat_id,
        message_id=224681,
        message_thread_id=update.message.message_thread_id
    )


@usage_limit
async def maptuke(update: Update, context):
    await context.bot.forward_message(
        chat_id=update.effective_chat.id,
        from_chat_id=bot_settings.chat_id,
        message_id=224682,
        message_thread_id=update.message.message_thread_id
    )


@usage_limit
async def map5p(update: Update, context):
    await context.bot.forward_message(
        chat_id=update.effective_chat.id,
        from_chat_id=bot_settings.chat_id,
        message_id=224683,
        message_thread_id=update.message.message_thread_id
    )


@usage_limit
async def studijne(update: Update, context):
    await context.bot.forward_message(
        chat_id=update.effective_chat.id,
        from_chat_id=bot_settings.chat_id,
        message_id=224684,
        message_thread_id=update.message.message_thread_id
    )


@usage_limit
async def schedule(update: Update, context):
    await context.bot.forward_message(
        chat_id=update.effective_chat.id,
        from_chat_id=bot_settings.chat_id,
        message_id=224685,
        message_thread_id=update.message.message_thread_id
    )


@usage_limit
async def invite(update: Update, context):
    if update.message:
        await update.message.reply_text(bot_settings.chat_link)


@usage_limit
async def week(update: Update, context):
    now = datetime.now()
    if now < bot_settings.semester_start:
        message = f"Semester sa začne {bot_settings.semester_start.strftime('%d.%m.%Y')}."
    else:
        current_week = ((now - bot_settings.semester_start).days // 7) + 1
        if current_week <= 13:
            message = f"Sme v {current_week}. týždni semestra."
        else:
            message = "Uvidíme sa neskor"
    await update.message.reply_text(message)
