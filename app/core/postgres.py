from aerich import Command
from telegram.ext import Application
from tortoise import Tortoise

from app.core.bot import bot_settings
from app.core.db import db_settings
from app.core.logger import logger

TORTOISE_ORM = {
    "connections": {"default": db_settings.url},
    "apps": {
        "models": {
            "models": ["app.persona.models", "app.community.models", "aerich.models"],
            "default_connection": "default",
        }
    },
    "use_tz": True,
    "timezone": bot_settings.TIMEZONE,
}


async def connect_db(app: Application) -> None:
    command = Command(tortoise_config=TORTOISE_ORM, app="models", location="./migrations")
    await command.init()
    applied = await command.upgrade(run_in_transaction=True)
    if applied:
        logger.info(f"Applied migrations: {applied}")
    else:
        logger.info("Database schema up to date")
    logger.info("Connected to database")


async def close_db(app: Application) -> None:
    await Tortoise.close_connections()
    logger.info("Closed connection to database")
