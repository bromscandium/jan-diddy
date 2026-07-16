from dataclasses import dataclass

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.bot import bot_settings


class LLMSettings(BaseSettings):
    PERSONA_ENGINE_URL: str = "http://localhost:8000"
    PERSONA_ENGINE_TIMEOUT: float = 120.0
    PERSONA_ENGINE_SECRET: str | None = None
    PERSONA_FORMAT: str = "flat"
    PERSONA_THREAD_ID: int | None = None
    BUFFER_SIZE: int = 100
    CAPTION_ENABLED: bool = True
    CAPTION_TIMEOUT: float = 120.0
    CAPTION_MAX_BYTES: int = 8_000_000
    REACT_ENABLED: bool = True
    REACT_COOLDOWN_SEC: int = 90
    GREET_ON_START: bool = True
    DOSSIER_AUTO_REFRESH: bool = False
    DOSSIER_REFRESH_EVERY: int = 100

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_nested_delimiter="__")


llm_settings = LLMSettings()


@dataclass(frozen=True)
class TrackConfig:
    min_messages: int
    min_minutes: int
    probability: float
    cooldown_minutes: int


@dataclass(frozen=True)
class TriggerConfig:
    active_hours: tuple[int, int]
    reply_probability: float
    prewarm_messages: int
    prewarm_minutes: int
    spontaneous: TrackConfig
    addressed: TrackConfig


PROD = TriggerConfig(
    active_hours=(8, 24),
    reply_probability=0.6,
    prewarm_messages=15,
    prewarm_minutes=25,
    spontaneous=TrackConfig(min_messages=20, min_minutes=30, probability=0.15, cooldown_minutes=20),
    addressed=TrackConfig(min_messages=2, min_minutes=0, probability=0.7, cooldown_minutes=3),
)

DEBUG = TriggerConfig(
    active_hours=(0, 24),
    reply_probability=0.5,
    prewarm_messages=1,
    prewarm_minutes=0,
    spontaneous=TrackConfig(min_messages=10, min_minutes=0, probability=1.0, cooldown_minutes=0),
    addressed=TrackConfig(min_messages=1, min_minutes=0, probability=1.0, cooldown_minutes=0),
)


def trigger_config() -> TriggerConfig:
    return DEBUG if bot_settings.DEBUG else PROD
