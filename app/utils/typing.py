import asyncio

from telegram import Bot, Message
from telegram.constants import ChatAction

TYPING_CHARS_PER_SECOND = 12.0
MIN_TYPING_SECONDS = 1.5
MAX_TYPING_SECONDS = 8.0
_REFRESH_SECONDS = 4.0


def typing_duration(text: str) -> float:
    seconds = len(text) / TYPING_CHARS_PER_SECOND
    return max(MIN_TYPING_SECONDS, min(MAX_TYPING_SECONDS, seconds))


async def type_then_send(
    bot: Bot,
    chat_id: int,
    text: str,
    message_thread_id: int | None = None,
    reply_to_message_id: int | None = None,
) -> Message:
    duration = typing_duration(text)
    elapsed = 0.0
    while elapsed < duration:
        await bot.send_chat_action(
            chat_id=chat_id,
            action=ChatAction.TYPING,
            message_thread_id=message_thread_id,
        )
        step = min(_REFRESH_SECONDS, duration - elapsed)
        await asyncio.sleep(step)
        elapsed += step

    return await bot.send_message(
        chat_id=chat_id,
        text=text,
        message_thread_id=message_thread_id,
        reply_to_message_id=reply_to_message_id,
    )
