from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        populate_by_name=True,
        env_nested_delimiter = "__"
    )


class DbSettings(BaseConfig):
    user: str
    password: str
    host: str
    port: int
    db: str

    @property
    def url(self) -> str:
        return f"postgres://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class BotSettings(BaseConfig):
    telegram_api_key: str
    weather_api_key: str
    chat_id: str
    admin_chat_id: str
    admin_ids: list[int]
    grant_admin_ids: list[int]
    reactions: list[str]
    semester_start: str
    chat_link: str
    db: DbSettings = Field(default_factory=DbSettings)

    @field_validator('semester_start')
    @classmethod
    def parse_semester_start(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, '%Y-%m-%d')
        return v


bot_settings = BotSettings()
