import sys

from loguru import logger

from app.core.bot import bot_settings

logger.remove()
logger.add(
    sys.stderr,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    ),
    level="DEBUG" if bot_settings.DEBUG else "INFO",
    enqueue=True
)
