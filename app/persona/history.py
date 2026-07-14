from datetime import UTC, datetime

from app.core.logger import logger
from app.persona.models import BotReplies, Messages


async def save_message(
    chat_id: int,
    thread_id: int | None,
    message_id: int,
    user_id: int | None,
    username: str,
    text: str,
    ts: int,
) -> None:
    try:
        await Messages.create(
            chat_id=chat_id,
            message_id=message_id,
            thread_id=thread_id,
            user_id=user_id,
            username=username,
            text=text,
            sent_at=datetime.fromtimestamp(ts, tz=UTC),
        )
    except Exception as exc:
        logger.warning(f"save_message failed: {exc}")


async def save_bot_reply(
    chat_id: int,
    thread_id: int | None,
    message_id: int | None,
    context: str,
    reply: str,
) -> None:
    try:
        await BotReplies.create(
            chat_id=chat_id,
            thread_id=thread_id,
            message_id=message_id,
            context=context,
            reply=reply,
        )
    except Exception as exc:
        logger.warning(f"save_bot_reply failed: {exc}")
