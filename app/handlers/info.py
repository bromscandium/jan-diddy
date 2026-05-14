from datetime import datetime

from telegram import Update
from telegram.ext import CallbackContext

from app.core.config import settings
from app.utils.decorators import usage_limit


@usage_limit
async def rules(update: Update, context: CallbackContext) -> None:
    if not update.message:
        return
    await update.message.reply_text(
        'čítali ste kanál <a href="https://t.me/c/2307996875/4/378327">ASAP</a>?', parse_mode="HTML"
    )


@usage_limit
async def moodle(update: Update, context: CallbackContext) -> None:
    await context.bot.forward_message(
        chat_id=update.effective_chat.id,
        from_chat_id=settings.CHAT_ID,
        message_id=378329,
        message_thread_id=update.message.message_thread_id,
    )


@usage_limit
async def links(update: Update, context: CallbackContext) -> None:
    await context.bot.forward_message(
        chat_id=update.effective_chat.id,
        from_chat_id=settings.CHAT_ID,
        message_id=378328,
        message_thread_id=update.message.message_thread_id,
    )


@usage_limit
async def scores(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        'Čítali ste kanál <a href="https://t.me/c/2307996875/4/378330">ASAP</a>?', parse_mode="HTML"
    )


@usage_limit
async def plan(update: Update, context: CallbackContext) -> None:
    await context.bot.forward_message(
        chat_id=update.effective_chat.id,
        from_chat_id=settings.CHAT_ID,
        message_id=378331,
        message_thread_id=update.message.message_thread_id,
    )


@usage_limit
async def maptuke(update: Update, context: CallbackContext) -> None:
    await context.bot.forward_message(
        chat_id=update.effective_chat.id,
        from_chat_id=settings.CHAT_ID,
        message_id=378332,
        message_thread_id=update.message.message_thread_id,
    )


@usage_limit
async def map5p(update: Update, context: CallbackContext) -> None:
    await context.bot.forward_message(
        chat_id=update.effective_chat.id,
        from_chat_id=settings.CHAT_ID,
        message_id=378333,
        message_thread_id=update.message.message_thread_id,
    )


@usage_limit
async def studijne(update: Update, context: CallbackContext) -> None:
    await context.bot.forward_message(
        chat_id=update.effective_chat.id,
        from_chat_id=settings.CHAT_ID,
        message_id=378334,
        message_thread_id=update.message.message_thread_id,
    )


@usage_limit
async def schedule(update: Update, context: CallbackContext) -> None:
    await context.bot.forward_message(
        chat_id=update.effective_chat.id,
        from_chat_id=settings.CHAT_ID,
        message_id=378335,
        message_thread_id=update.message.message_thread_id,
    )


@usage_limit
async def invite(update: Update, context: CallbackContext) -> None:
    if update.message:
        await update.message.reply_text(settings.CHAT_LINK)


@usage_limit
async def week(update: Update, context: CallbackContext) -> None:
    now = datetime.now().date()
    if now < settings.SEMESTER_START:
        message = f"Semester sa začne {settings.SEMESTER_START.strftime('%d.%m.%Y')}."
    else:
        current_week = ((now - settings.SEMESTER_START).days // 7) + 1
        if current_week <= 13:
            message = f"Sme v {current_week}. týždni semestra. 💀"
        else:
            message = "Uvidíme sa neskor na medziroku. 💀"
    await update.message.reply_text(message)
