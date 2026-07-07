import json
import re

from app.core.logger import logger
from app.core.redis import redis
from app.persona.models import SuccessfulDialogs
from app.persona.services import profiles

REACTION_WEIGHTS = {
    "😂": 3, "🤣": 3, "🔥": 2, "❤": 1, "❤️": 1, "👍": 1, "👏": 1,
    "👎": -2, "💩": -2, "🤡": -2, "🤮": -3, "🤢": -3,
}

KEYWORD_WEIGHTS = {
    "ахаха": 3, "ахах": 3, "хаха": 2, "хах": 2, "ржу": 3, "ржач": 3, "угар": 3,
    "орну": 3, "ору": 3, "орж": 3, "лол": 2, "кек": 2,
    "база": 2, "збс": 2, "огонь": 2, "вогонь": 2, "пушка": 2, "красав": 2, "топчик": 2,
    "ахує": 3, "охує": 3, "заєбіс": 3, "заебис": 3, "піздат": 3, "пиздат": 3,
    "піздєц": 2, "піздець": 2, "пиздец": 2, "пздц": 2,
    "хуйн": -3, "гівн": -3, "говн": -3, "днищ": -2, "кринж": -2, "cringe": -2,
    "скам": -2, "херн": -1, "хєрн": -1, "фігн": -1,
}
SCORING_WINDOW = 120


def keyword_score(text: str) -> int:
    total = 0
    for word in re.findall(r"\w+", text.lower()):
        for root, weight in KEYWORD_WEIGHTS.items():
            if root in word:
                total += weight
                break
    return total


def has_signal(text: str) -> bool:
    return keyword_score(text) != 0


def _pending_key(chat_id: int, bot_message_id: int) -> str:
    return f"jd:pending:{chat_id}:{bot_message_id}"


def _lastbot_key(chat_id: int, thread_id: int | None) -> str:
    return f"jd:lastbot:{chat_id}:{thread_id if thread_id is not None else 'none'}"


def is_approval(text: str) -> bool:
    low = text.lower()
    return any(k in low for k in APPROVAL_KEYWORDS)


async def register_pending(
    chat_id: int,
    thread_id: int | None,
    bot_message_id: int,
    context: str,
    reply: str,
    target_user_id: int | None,
    target_username: str = "",
) -> None:
    payload = json.dumps(
        {
            "chat_id": chat_id,
            "context": context,
            "reply": reply,
            "target_user_id": target_user_id,
            "target_username": target_username,
            "score": 0,
            "row_id": None,
        }
    )
    pipe = redis().pipeline()
    pipe.set(_pending_key(chat_id, bot_message_id), payload, ex=SCORING_WINDOW + 30)
    pipe.set(_lastbot_key(chat_id, thread_id), bot_message_id, ex=SCORING_WINDOW)
    await pipe.execute()


async def last_bot_message(chat_id: int, thread_id: int | None) -> int | None:
    v = await redis().get(_lastbot_key(chat_id, thread_id))
    return int(v) if v else None


async def _add_score(chat_id: int, bot_message_id: int, delta: int) -> None:
    r = redis()
    key = _pending_key(chat_id, bot_message_id)
    raw = await r.get(key)
    if not raw:
        return
    data = json.loads(raw)
    data["score"] += delta
    try:
        if data["row_id"]:
            await SuccessfulDialogs.filter(id=data["row_id"]).update(score=data["score"])
        else:
            row = await SuccessfulDialogs.create(
                chat_id=chat_id, context=data["context"], reply=data["reply"], score=data["score"]
            )
            data["row_id"] = row.id
    except Exception as exc:
        logger.warning(f"scoring persist failed: {exc}")
    await r.set(key, json.dumps(data), ex=SCORING_WINDOW + 30)
    await profiles.record(data.get("target_user_id"), data.get("target_username", ""), delta)


async def apply_reaction(chat_id: int, bot_message_id: int, emoji: str) -> None:
    await _add_score(chat_id, bot_message_id, REACTION_WEIGHTS.get(emoji, 1))


async def apply_reply_signal(chat_id: int, bot_message_id: int, text: str) -> None:
    ks = keyword_score(text)
    await _add_score(chat_id, bot_message_id, ks if ks else 1)
