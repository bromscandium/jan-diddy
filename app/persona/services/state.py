import json

from app.core.llm import llm_settings
from app.core.redis import redis


def _prefix(chat_id: int, thread_id: int | None) -> str:
    return f"jd:{chat_id}:{thread_id if thread_id is not None else 'none'}"


async def record_incoming(
    chat_id: int,
    thread_id: int | None,
    username: str,
    text: str,
    message_id: int,
    ts: int,
) -> None:
    r = redis()
    p = _prefix(chat_id, thread_id)
    item = json.dumps({"username": username, "text": text, "message_id": message_id, "ts": ts})
    pipe = r.pipeline()
    pipe.lpush(f"{p}:buf", item)
    pipe.ltrim(f"{p}:buf", 0, llm_settings.BUFFER_SIZE - 1)
    pipe.hincrby(f"{p}:state", "count", 1)
    pipe.hset(f"{p}:state", "last_activity_ts", ts)
    await pipe.execute()


async def get_context(chat_id: int, thread_id: int | None) -> list[dict]:
    r = redis()
    raw = await r.lrange(f"{_prefix(chat_id, thread_id)}:buf", 0, llm_settings.BUFFER_SIZE - 1)
    items = [json.loads(x) for x in raw]
    items.reverse()
    return items


async def get_state(chat_id: int, thread_id: int | None) -> dict:
    r = redis()
    h = await r.hgetall(f"{_prefix(chat_id, thread_id)}:state")
    return {
        "count": int(h.get("count", 0)),
        "last_response_ts": float(h.get("last_response_ts", 0)),
        "cooldown_until": float(h.get("cooldown_until", 0)),
        "prewarmed": h.get("prewarmed") == "1",
    }


async def mark_prewarmed(chat_id: int, thread_id: int | None) -> None:
    r = redis()
    await r.hset(f"{_prefix(chat_id, thread_id)}:state", "prewarmed", "1")


async def register_reply(chat_id: int, thread_id: int | None, now: float, cooldown_minutes: int) -> None:
    r = redis()
    await r.hset(
        f"{_prefix(chat_id, thread_id)}:state",
        mapping={
            "count": 0,
            "last_response_ts": now,
            "cooldown_until": now + cooldown_minutes * 60,
            "prewarmed": "0",
        },
    )
