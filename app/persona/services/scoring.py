import json

from app.core.logger import logger
from app.core.redis import redis
from app.persona.models import SuccessfulDialogs

SUCCESS_KEYWORDS = {
    "ахаха", "ахах", "хаха", "хах", "ору", "орнув", "орнула", "ржу",
    "лол", "кек", "база", "збс", "топ", "😂", "🤣", "💀", "🔥",
}
SCORING_WINDOW = 120


def _pending_key(chat_id: int, bot_message_id: int) -> str:
    return f"jd:pending:{chat_id}:{bot_message_id}"


def _lastbot_key(chat_id: int, thread_id: int | None) -> str:
    return f"jd:lastbot:{chat_id}:{thread_id if thread_id is not None else 'none'}"


def contains_success_keyword(text: str) -> bool:
    low = text.lower()
    return any(k in low for k in SUCCESS_KEYWORDS)


async def register_pending(
    chat_id: int,
    thread_id: int | None,
    bot_message_id: int,
    context: str,
    reply: str,
) -> None:
    r = redis()
    payload = json.dumps({"chat_id": chat_id, "context": context, "reply": reply, "saved": 0})
    pipe = r.pipeline()
    pipe.set(_pending_key(chat_id, bot_message_id), payload, ex=SCORING_WINDOW + 30)
    pipe.set(_lastbot_key(chat_id, thread_id), bot_message_id, ex=SCORING_WINDOW)
    await pipe.execute()


async def last_bot_message(chat_id: int, thread_id: int | None) -> int | None:
    v = await redis().get(_lastbot_key(chat_id, thread_id))
    return int(v) if v else None


async def mark_success(chat_id: int, bot_message_id: int, weight: int = 1) -> None:
    r = redis()
    key = _pending_key(chat_id, bot_message_id)
    raw = await r.get(key)
    if not raw:
        return
    data = json.loads(raw)
    if data.get("saved"):
        return
    data["saved"] = 1
    await r.set(key, json.dumps(data), ex=SCORING_WINDOW + 30)
    try:
        await SuccessfulDialogs.create(
            chat_id=chat_id,
            context=data["context"],
            reply=data["reply"],
            score=weight,
        )
    except Exception as exc:
        logger.warning(f"save successful dialog failed: {exc}")
