import httpx
from telegram import Update
from telegram.error import NetworkError
from telegram.ext import Application, ApplicationBuilder, CallbackContext

from app.core.bot import bot_settings
from app.core.http import close_http_session, init_http_session
from app.core.logger import logger
from app.core.postgres import close_db, connect_db
from app.core.redis import close_redis, init_redis
from app.handlers import setup_handlers


class BotApplication:
    def __init__(self) -> None:
        self.app: Application = (
            ApplicationBuilder()
            .token(bot_settings.BOT_TOKEN)
            .post_init(self._on_startup)
            .post_shutdown(self._on_shutdown)
            .build()
        )
        setup_handlers(self.app)
        self.app.add_error_handler(self._on_error)

    async def _on_startup(self, app: Application) -> None:
        await connect_db(app)
        await init_redis()
        await init_http_session()
        logger.info("Bot started successfully")
        await self._notify_admin(app, "Bot started successfully")

    async def _on_shutdown(self, app: Application) -> None:
        await close_db(app)
        await close_redis()
        await close_http_session()
        logger.info("Bot shut down")
        await self._notify_admin(app, "Bot shut down")

    async def _notify_admin(self, app: Application, text: str) -> None:
        try:
            await app.bot.send_message(chat_id=bot_settings.ADMIN_CHAT_ID, text=text)
        except Exception as exc:
            logger.warning(f"admin notify failed ({text!r}): {exc!r}")

    async def _on_error(self, update: object, context: CallbackContext) -> None:
        error = context.error
        logger.error(f"Exception while handling an update: {error}")

        if "Conflict: terminated by other getUpdates request" in str(error):
            logger.warning("Bot instance conflict detected. Exiting to allow orchestrator restart.")
            return

        if isinstance(error, (NetworkError, httpx.TransportError)) or "Bad Gateway" in str(error):
            logger.warning(f"Transient network error, skipping admin report: {error!r}")
            return

        try:
            await context.bot.send_message(chat_id=bot_settings.ADMIN_CHAT_ID, text=f"Bot error: {error}")
        except Exception as e:
            logger.error(f"Failed to send error report: {e}")

    def run(self) -> None:
        if bot_settings.webhook_url:
            logger.info("Starting Telegram Bot (webhook)...")
            self.app.run_webhook(
                listen="0.0.0.0",
                port=bot_settings.PORT,
                url_path=bot_settings.WEBHOOK_PATH,
                webhook_url=f"{bot_settings.webhook_url}/{bot_settings.WEBHOOK_PATH}",
                secret_token=bot_settings.WEBHOOK_SECRET,
                drop_pending_updates=True,
                allowed_updates=Update.ALL_TYPES,
            )
        else:
            logger.info("Starting Telegram Bot (polling fallback)...")
            self.app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
