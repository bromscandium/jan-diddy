from datetime import date

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    WEATHER_API_KEY: str
    CHAT_ID: int
    ADMIN_CHAT_ID: int
    ADMIN_IDS: list[int]
    GRANT_ADMIN_IDS: list[int]
    REACTIONS: list[str]
    SEMESTER_START: date
    CHAT_LINK: str
    TIMEZONE: str = "Europe/London"
    BANNED_BY_ID: list[int]

    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    DB: str

    @property
    def url(self) -> str:
        return f"postgres://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_nested_delimiter="__")


settings = Settings()  # type: ignore
