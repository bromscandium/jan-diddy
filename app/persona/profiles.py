from datetime import UTC, datetime

from app.core.logger import logger
from app.core.redis import redis
from app.persona.models import UserProfiles


def _key(user_id: int) -> str:
    return f"jd:profile:{user_id}"


async def mark_replied(user_id: int | None, username: str) -> None:
    if user_id is None:
        return
    try:
        profile, _ = await UserProfiles.get_or_create(user_id=user_id, defaults={"username": username})
        profile.replies_to_them += 1
        profile.username = username
        profile.last_seen = datetime.now(UTC)
        await profile.save()
    except Exception as exc:
        logger.warning(f"profiles.mark_replied failed: {exc}")


async def record(user_id: int | None, username: str, delta: int) -> None:
    if user_id is None:
        return
    try:
        profile, _ = await UserProfiles.get_or_create(user_id=user_id, defaults={"username": username})
        profile.engagement_score += delta
        profile.username = username
        profile.last_seen = datetime.now(UTC)
        if delta > 0:
            profile.successes += 1
        await profile.save()
        await redis().hset(_key(user_id), mapping={"engagement_score": profile.engagement_score})
    except Exception as exc:
        logger.warning(f"profiles.record failed: {exc}")


async def get(user_id: int | None) -> dict:
    if user_id is None:
        return {"engagement_score": 0}
    try:
        cached = await redis().hgetall(_key(user_id))
        if cached:
            return {"engagement_score": int(cached.get("engagement_score", 0))}
        profile = await UserProfiles.get_or_none(user_id=user_id)
        return {"engagement_score": profile.engagement_score if profile else 0}
    except Exception as exc:
        logger.warning(f"profiles.get failed: {exc}")
        return {"engagement_score": 0}


async def bias(user_id: int | None) -> float:
    score = (await get(user_id))["engagement_score"]
    return 1.0 + max(-0.5, min(1.0, score / 20.0))
