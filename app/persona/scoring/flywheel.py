import json
import time

from tortoise.expressions import F

from app.core.logger import logger
from app.core.redis import redis
from app.persona import profiles, state
from app.persona.models import SuccessfulDialogs
from app.persona.scoring.keys import (
    IGNORED_ACTIVITY_MIN,
    PENDING_META_TTL,
    SCORING_WINDOW,
    idx_key,
    lastbot_key,
    meta_key,
)
from app.persona.scoring.rules import reaction_score, reply_score


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
    pipe.set(meta_key(chat_id, bot_message_id), meta, ex=PENDING_META_TTL)
    pipe.set(lastbot_key(chat_id, thread_id), bot_message_id, ex=SCORING_WINDOW)
    pipe.zadd(idx_key(chat_id, thread_id), {str(bot_message_id): created + SCORING_WINDOW})
    await pipe.execute()


async def last_bot_message(chat_id: int, thread_id: int | None) -> int | None:
    v = await redis().get(lastbot_key(chat_id, thread_id))
    return int(v) if v else None


async def _add_score(chat_id: int, bot_message_id: int, delta: int, source: str) -> None:
    raw = await redis().get(meta_key(chat_id, bot_message_id))
    if not raw:
        logger.info(f"scoring: {source} ({delta:+d}) on msg {bot_message_id} — not a bot reply / expired, skipped")
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
            await redis().set(meta_key(chat_id, bot_message_id), json.dumps(meta), ex=PENDING_META_TTL)
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
    delta = reply_score(text)
    if delta == 0:
        return
    await _add_score(chat_id, bot_message_id, delta, f"reply {text[:40]!r}")


async def sweep_ignored(chat_id: int, thread_id: int | None, now_ts: int) -> None:
    idx = idx_key(chat_id, thread_id)
    r = redis()
    due = await r.zrangebyscore(idx, "-inf", now_ts)
    for member in due:
        bot_message_id = int(member)
        raw = await r.get(meta_key(chat_id, bot_message_id))
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
        await r.delete(meta_key(chat_id, bot_message_id))
