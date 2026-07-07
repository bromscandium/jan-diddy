import redis.asyncio as aioredis
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    REDIS_URL: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_nested_delimiter="__")


redis_settings = RedisSettings()


class RedisClient:
    client: aioredis.Redis | None = None


async def init_redis() -> None:
    if RedisClient.client is None:
        RedisClient.client = aioredis.from_url(redis_settings.REDIS_URL, decode_responses=True)


async def close_redis() -> None:
    if RedisClient.client is not None:
        await RedisClient.client.aclose()
        RedisClient.client = None


def redis() -> aioredis.Redis:
    if RedisClient.client is None:
        raise RuntimeError("Redis is not initialized")
    return RedisClient.client
