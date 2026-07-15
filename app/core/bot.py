from datetime import date

from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    BOT_TOKEN: str
    WEATHER_API_KEY: str
    CHAT_ID: int
    ADMIN_CHAT_ID: int
    ADMIN_IDS: list[int]
    SEMESTER_START: date
    CHAT_LINK: str
    TIMEZONE: str = "Europe/London"
    BANNED_BY_ID: list[int] = []
    DEBUG: bool = False

    PORT: int = 8080
    WEBHOOK_DOMAIN: str | None = None
    WEBHOOK_PATH: str = "webhook"
    WEBHOOK_SECRET: str | None = None

    @property
    def webhook_url(self) -> str | None:
        if not self.WEBHOOK_DOMAIN:
            return None
        return f"https://{self.WEBHOOK_DOMAIN}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_nested_delimiter="__")


bot_settings = BotSettings()  # type: ignore
