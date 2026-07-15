from app.core.llm import llm_settings
from app.core.logger import logger
from app.core.redis import redis
from app.persona import client, state
from app.persona.orchestrator.ingest import identity


def _cooldown_key(chat_id: int, thread_id: int | None) -> str:
    return f"jd:{chat_id}:{thread_id if thread_id is not None else 'none'}:react_cd"


async def maybe_react(bot, msg) -> None:
    if not llm_settings.REACT_ENABLED:
        return
    key = _cooldown_key(msg.chat_id, msg.message_thread_id)
    if await redis().set(key, "1", ex=llm_settings.REACT_COOLDOWN_SEC, nx=True) is None:
        return
    emoji = await reaction_emoji(msg)
    if not emoji:
        return
    try:
        await bot.set_message_reaction(
            chat_id=msg.chat_id, message_id=msg.message_id, reaction=emoji, is_big=False
        )
    except Exception as exc:
        logger.warning(f"set reaction failed: {exc}")


async def reaction_emoji(msg) -> str | None:
    user_id, username, ts = identity(msg)
    ctx = await state.get_context(msg.chat_id, msg.message_thread_id)
    payload = [
        {
            "username": m["username"],
            "text": m["text"],
            "ts": m.get("ts"),
            "user_id": m.get("user_id"),
            "message_id": m.get("message_id"),
            "reply_to": m.get("reply_to"),
        }
        for m in ctx
    ]
    text = msg.text or msg.caption or ""
    if text and (not payload or payload[-1].get("message_id") != msg.message_id):
        payload.append(
            {
                "username": username,
                "text": text,
                "ts": ts,
                "user_id": user_id,
                "message_id": msg.message_id,
                "reply_to": None,
            }
        )
    if not any(p["text"] for p in payload):
        return None
    return await client.react(payload, msg.chat_id)
