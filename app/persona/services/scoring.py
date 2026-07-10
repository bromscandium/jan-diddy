import json
import time

from tortoise.expressions import F

from app.core.logger import logger
from app.core.redis import redis
from app.persona.models import SuccessfulDialogs
from app.persona.services import profiles, state

LAUGH = [
    "ахаха", "ахах", "хаха", "хах", "ржу", "ржач", "ржал", "угар", "орну", "орж", "ору",
    "лол", "кек", "хихи", "хіхі", "гыгы", "гигі", "лмао", "lmao", "lol",
]
APPROVAL = [
    "база", "збс", "огонь", "вогонь", "агонь", "пушка", "красав", "топчик", "топово",
    "ахує", "охує", "заєбіс", "заебис", "заєбок", "піздат", "пиздат",
    "імба", "імбов", "кайф", "жиза", "вайб", "найс", "nice", "супер", "круто", "крутяк",
    "класн", "бомба", "бомбов", "мощно", "потужн", "красота", "молодц", "молодець", "респект",
    "прикол", "смішн", "смешн", "шедевр", "легендар", "гені", "чітко", "четко", "норм", "гарно", "зарош",
]
NEGATIVE = [
    "не смішн", "не смешн", "нудн", "душнил", "душніл", "маячн", "бред", "нецікав", "неинтересн",
    "не в тему", "не то", "фейл", "fail", "провал", "скучн", "зевот", "розчарув", "разочаров",
    "тупизн", "тупак", "відстій", "відстой", "скам", "не зайшл", "не смешно", "мимо кас",
]
AMBIGUOUS = [
    "хуйн", "гівн", "говн", "кринж", "cringe", "зашквар", "днищ", "пздц", "піздєц", "піздець",
    "пиздец", "лажа", "жесть", "капец", "капець", "трэш", "треш", "трешак",
    "даун", "дебіл", "ідіот", "чмо", "клоун", "дурак", "лошар", "фігн", "херн", "хєрн",
]

ENGAGEMENT_EMOJI = {"😂", "🤣", "🔥", "❤", "❤️", "👍", "👏", "💯", "🫡"}
NEGATIVE_EMOJI = {"🤮", "🤢", "🥱"}
AMBIGUOUS_EMOJI = {"🤡", "👎", "💩"}

SCORING_WINDOW = 120
IGNORED_ACTIVITY_MIN = 3
PENDING_META_TTL = 7200


def _roots(text: str, roots: list[str]) -> int:
    low = text.lower()
    return sum(1 for r in roots if r in low)


def _emoji(text: str, chars: set[str]) -> int:
    return sum(text.count(c) for c in chars)


def is_quality_mark(text: str) -> bool:
    return text.strip().lower().startswith("/q")


def has_signal(text: str) -> bool:
    if is_quality_mark(text):
        return True
    return bool(
        _roots(text, LAUGH) or _roots(text, APPROVAL) or _roots(text, NEGATIVE) or _roots(text, AMBIGUOUS)
        or _emoji(text, ENGAGEMENT_EMOJI) or _emoji(text, NEGATIVE_EMOJI) or _emoji(text, AMBIGUOUS_EMOJI)
    )


def reply_score(text: str) -> int:
    if is_quality_mark(text):
        return 5
    laugh = _roots(text, LAUGH) + _emoji(text, ENGAGEMENT_EMOJI)
    appr = _roots(text, APPROVAL)
    neg = _roots(text, NEGATIVE) + _emoji(text, NEGATIVE_EMOJI)
    amb = _roots(text, AMBIGUOUS) + _emoji(text, AMBIGUOUS_EMOJI)
    if laugh:
        return max(1, 2 + min(laugh, 3) + min(appr, 1) - min(neg, 2))
    if neg:
        return -(2 + min(neg, 2))
    if appr:
        return max(1, 1 + min(appr, 3))
    if amb:
        return -1
    return 1


def reaction_score(emoji: str) -> int:
    if emoji in ENGAGEMENT_EMOJI:
        return 3
    if emoji in NEGATIVE_EMOJI:
        return -3
    if emoji in AMBIGUOUS_EMOJI:
        return -1
    return 1


def _meta_key(chat_id: int, bot_message_id: int) -> str:
    return f"jd:pendmeta:{chat_id}:{bot_message_id}"


def _idx_key(chat_id: int, thread_id: int | None) -> str:
    return f"jd:pendidx:{chat_id}:{thread_id if thread_id is not None else 'none'}"


def _lastbot_key(chat_id: int, thread_id: int | None) -> str:
    return f"jd:lastbot:{chat_id}:{thread_id if thread_id is not None else 'none'}"


async def register_pending(
    chat_id: int,
    thread_id: int | None,
    bot_message_id: int,
    context: str,
    reply: str,
    target_user_id: int | None,
    target_username: str = "",
    topic: str | None = None,
) -> None:
    created = int(time.time())
    row_id = None
    try:
        row = await SuccessfulDialogs.create(
            chat_id=chat_id,
            thread_id=thread_id,
            user_id=target_user_id,
            topic=topic,
            context=context,
            reply=reply,
            score=0,
        )
        row_id = row.id
    except Exception as exc:
        logger.warning(f"pending row create failed: {exc}")
    meta = json.dumps(
        {
            "row_id": row_id,
            "created": created,
            "thread_id": thread_id,
            "topic": topic,
            "context": context,
            "reply": reply,
            "target_user_id": target_user_id,
            "target_username": target_username,
        }
    )
    pipe = redis().pipeline()
    pipe.set(_meta_key(chat_id, bot_message_id), meta, ex=PENDING_META_TTL)
    pipe.set(_lastbot_key(chat_id, thread_id), bot_message_id, ex=SCORING_WINDOW)
    pipe.zadd(_idx_key(chat_id, thread_id), {str(bot_message_id): created + SCORING_WINDOW})
    await pipe.execute()


async def last_bot_message(chat_id: int, thread_id: int | None) -> int | None:
    v = await redis().get(_lastbot_key(chat_id, thread_id))
    return int(v) if v else None


async def _add_score(chat_id: int, bot_message_id: int, delta: int, source: str) -> None:
    raw = await redis().get(_meta_key(chat_id, bot_message_id))
    if not raw:
        logger.info(f"scoring: {source} ({delta:+d}) on bot msg {bot_message_id} — window closed, skipped")
        return
    meta = json.loads(raw)
    row_id = meta.get("row_id")
    try:
        if row_id is None:
            row = await SuccessfulDialogs.create(
                chat_id=chat_id,
                thread_id=meta.get("thread_id"),
                user_id=meta.get("target_user_id"),
                topic=meta.get("topic"),
                context=meta.get("context", ""),
                reply=meta.get("reply", ""),
                score=delta,
            )
            meta["row_id"] = row.id
            await redis().set(_meta_key(chat_id, bot_message_id), json.dumps(meta), ex=PENDING_META_TTL)
        else:
            await SuccessfulDialogs.filter(id=row_id).update(score=F("score") + delta)
            row = await SuccessfulDialogs.filter(id=row_id).first()
    except Exception as exc:
        logger.warning(f"scoring persist failed: {exc}")
        return
    total = row.score if row else "?"
    logger.info(f"scoring: {source} ({delta:+d}) on bot msg {bot_message_id} → total {total}")
    await profiles.record(meta.get("target_user_id"), meta.get("target_username", ""), delta)


async def apply_reaction(chat_id: int, bot_message_id: int, emoji: str) -> None:
    await _add_score(chat_id, bot_message_id, reaction_score(emoji), f"reaction {emoji}")


async def apply_reply_signal(chat_id: int, bot_message_id: int, text: str) -> None:
    await _add_score(chat_id, bot_message_id, reply_score(text), f"reply {text[:40]!r}")


async def sweep_ignored(chat_id: int, thread_id: int | None, now_ts: int) -> None:
    idx = _idx_key(chat_id, thread_id)
    r = redis()
    due = await r.zrangebyscore(idx, "-inf", now_ts)
    for member in due:
        bot_message_id = int(member)
        raw = await r.get(_meta_key(chat_id, bot_message_id))
        if raw:
            meta = json.loads(raw)
            row_id = meta.get("row_id")
            created = meta.get("created", 0)
            if row_id is not None:
                try:
                    active = await state.count_after(chat_id, thread_id, created, created + SCORING_WINDOW)
                    if active >= IGNORED_ACTIVITY_MIN:
                        await SuccessfulDialogs.filter(id=row_id, score=0).update(score=-1)
                        logger.info(f"scoring: ignored (-1) on bot msg {bot_message_id} (row {row_id})")
                except Exception as exc:
                    logger.warning(f"sweep finalize failed: {exc}")
        await r.zrem(idx, member)
        await r.delete(_meta_key(chat_id, bot_message_id))
