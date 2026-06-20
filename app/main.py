import httpx
from telegram.error import NetworkError
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
    error = context.error
    logger.error(f"Exception while handling an update: {error}")
    
    if "Conflict: terminated by other getUpdates request" in str(error):
        logger.warning("Bot instance conflict detected. Exiting to allow orchestrator restart.")
        return

    if (
        isinstance(error, (NetworkError, httpx.TransportError))
        or "Bad Gateway" in str(error)
    ):
        logger.warning(f"Transient network error, skipping admin report: {error!r}")
        return

    try:
        await context.bot.send_message(
            chat_id=settings.ADMIN_CHAT_ID,
            text=f"Bot error: {error}",
        )
    except Exception as e:
        logger.error(f"Failed to send error report: {e}")


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

    if settings.webhook_url:
        logger.info("Starting Telegram Bot (webhook)...")
        bot.run_webhook(
            listen="0.0.0.0",
            port=settings.PORT,
            url_path=settings.WEBHOOK_PATH,
            webhook_url=f"{settings.webhook_url}/{settings.WEBHOOK_PATH}",
            secret_token=settings.WEBHOOK_SECRET,
            drop_pending_updates=True,
        )
    else:
        logger.info("Starting Telegram Bot (polling fallback)...")
        bot.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
