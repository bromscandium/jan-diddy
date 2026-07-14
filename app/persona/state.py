import json

from app.core.llm import llm_settings
from app.core.redis import redis

TRACKS = ("spont", "addr")


def _prefix(chat_id: int, thread_id: int | None) -> str:
    return f"jd:{chat_id}:{thread_id if thread_id is not None else 'none'}"


async def record_incoming(
    chat_id: int,
    thread_id: int | None,
    user_id: int | None,
    username: str,
    text: str,
    message_id: int,
    ts: int,
    reply_to: int | None = None,
) -> None:
    r = redis()
    p = _prefix(chat_id, thread_id)
    item = json.dumps(
        {
            "user_id": user_id,
            "username": username,
            "text": text,
            "message_id": message_id,
            "ts": ts,
            "reply_to": reply_to,
        }
    )
    pipe = r.pipeline()
    pipe.lpush(f"{p}:buf", item)
    pipe.ltrim(f"{p}:buf", 0, llm_settings.BUFFER_SIZE - 1)
    for track in TRACKS:
        pipe.hincrby(f"{p}:{track}", "count", 1)
    pipe.hset(f"{p}:spont", "last_activity_ts", ts)
    await pipe.execute()


async def get_context(chat_id: int, thread_id: int | None) -> list[dict]:
    r = redis()
    raw = await r.lrange(f"{_prefix(chat_id, thread_id)}:buf", 0, llm_settings.BUFFER_SIZE - 1)
    items = [json.loads(x) for x in raw]
    items.reverse()
    return items


async def count_after(chat_id: int, thread_id: int | None, ts_cutoff: int, ts_until: int | None = None) -> int:
    raw = await redis().lrange(f"{_prefix(chat_id, thread_id)}:buf", 0, llm_settings.BUFFER_SIZE - 1)
    total = 0
    for x in raw:
        try:
            ts = json.loads(x).get("ts", 0)
        except (ValueError, TypeError):
            continue
        if ts > ts_cutoff and (ts_until is None or ts <= ts_until):
            total += 1
    return total


async def get_track(chat_id: int, thread_id: int | None, track: str) -> dict:
    h = await redis().hgetall(f"{_prefix(chat_id, thread_id)}:{track}")
    return {
        "count": int(h.get("count", 0)),
        "last_response_ts": float(h.get("last_response_ts", 0)),
        "cooldown_until": float(h.get("cooldown_until", 0)),
        "prewarmed": h.get("prewarmed") == "1",
    }


async def mark_prewarmed(chat_id: int, thread_id: int | None) -> None:
    await redis().hset(f"{_prefix(chat_id, thread_id)}:spont", "prewarmed", "1")


async def register_reply(
    chat_id: int, thread_id: int | None, track: str, now: float, cooldown_minutes: int
) -> None:
    await redis().hset(
        f"{_prefix(chat_id, thread_id)}:{track}",
        mapping={
            "count": 0,
            "last_response_ts": now,
            "cooldown_until": now + cooldown_minutes * 60,
            "prewarmed": "0",
        },
    )
