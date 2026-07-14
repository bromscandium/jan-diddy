import time

from app.core.llm import llm_settings
from app.persona import history, state


def identity(msg) -> tuple[int | None, str, int]:
    user = msg.from_user
    user_id = user.id if user else None
    username = user.full_name if user else "anon"
    ts = int(msg.date.timestamp()) if msg.date else int(time.time())
    return user_id, username, ts


def in_persona_thread(msg) -> bool:
    if not msg or msg.message_thread_id != llm_settings.PERSONA_THREAD_ID:
        return False
    user = msg.from_user
    return not (user and user.is_bot)


async def ingest(msg, text: str, reply_to_id: int | None = None) -> tuple[int | None, str, int]:
    user_id, username, ts = identity(msg)
    await state.record_incoming(
        msg.chat_id, msg.message_thread_id, user_id, username, text, msg.message_id, ts, reply_to_id
    )
    await history.save_message(msg.chat_id, msg.message_thread_id, msg.message_id, user_id, username, text, ts)
    return user_id, username, ts
