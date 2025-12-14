from tortoise import Tortoise
from telegram.ext import Application
from app.core.config import bot_settings

TORTOISE_ORM = {
    "connections": {
        "default": bot_settings.db.url
    },
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default"
        }
    }
}

async def connect_db(app: Application) -> None:
    await Tortoise.init(config=TORTOISE_ORM)
    print("Connected to database")

async def close_db(app: Application) -> None:
    await Tortoise.close_connections()
    print("Closed connection to database")