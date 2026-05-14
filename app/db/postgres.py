from telegram.ext import Application
from tortoise import Tortoise

from app.core.config import settings
from app.core.logger import logger

TORTOISE_ORM = {
    "connections": {"default": settings.url},
    "apps": {"models": {"models": ["app.models", "aerich.models"], "default_connection": "default"}},
    "use_tz": True,
    "timezone": settings.TIMEZONE,
}


async def connect_db(app: Application) -> None:
    await Tortoise.init(config=TORTOISE_ORM)
    logger.info("Connected to database")


async def close_db(app: Application) -> None:
    await Tortoise.close_connections()
    logger.info("Closed connection to database")
