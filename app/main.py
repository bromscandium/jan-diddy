from telegram.ext import ApplicationBuilder, CallbackContext

from app.core.config import settings
from app.core.http import close_http_session, init_http_session
from app.core.logger import logger
from app.db.postgres import close_db, connect_db
from app.handlers import setup_handlers


async def on_startup(app) -> None:
    await connect_db(app)
    await init_http_session()
    logger.info("Bot started successfully")
    await app.bot.send_message(chat_id=settings.ADMIN_CHAT_ID, text="Bot started successfully")


async def on_shutdown(app) -> None:
    await close_db(app)
    await close_http_session()
    logger.info("Bot shut down")
    await app.bot.send_message(chat_id=settings.ADMIN_CHAT_ID, text="Bot shut down")


async def error_handler(update: object, context: CallbackContext) -> None:
    logger.exception("Exception while handling an update:")
    try:
        await context.bot.send_message(
            chat_id=settings.ADMIN_CHAT_ID,
            text=f"Bot error: {context.error}",
        )
    except Exception:
        logger.error("Failed to send error report to admin group")


def main() -> None:
    bot = (
        ApplicationBuilder()
        .token(settings.BOT_TOKEN)
        .post_init(on_startup)
        .post_shutdown(on_shutdown)
        .build()
    )

    setup_handlers(bot)
    bot.add_error_handler(error_handler)

    logger.info("Starting Telegram Bot...")
    bot.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
