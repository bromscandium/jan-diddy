import asyncio
import time
import functools
from telegram.ext import CallbackContext
from telegram import Update

_USER_LAST_CALLED = {}
_COMMAND_USAGE = {}


def personal_limit(seconds: int):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
            user_id = update.effective_user.id
            key = (user_id, func.__name__)
            now = time.time()
            last = _USER_LAST_CALLED.get(key, 0)
            if now - last < seconds:
                return None
            _USER_LAST_CALLED[key] = now
            return await func(update, context, *args, **kwargs)

        return wrapper

    return decorator


def usage_limit(func):
    @functools.wraps(func)
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = update.effective_user.id
        command = func.__name__
        usage = _COMMAND_USAGE.setdefault(user_id, {}).setdefault(command, 0)

        if usage >= 2:
            return None

        _COMMAND_USAGE[user_id][command] += 1
        asyncio.create_task(_reset_usage(user_id, command))
        return await func(update, context, *args, **kwargs)

    return wrapper


async def _reset_usage(user_id: int, command: str):
    await asyncio.sleep(300)
    if user_id in _COMMAND_USAGE and command in _COMMAND_USAGE[user_id]:
        _COMMAND_USAGE[user_id][command] -= 1
        if _COMMAND_USAGE[user_id][command] <= 0:
            del _COMMAND_USAGE[user_id][command]
        if not _COMMAND_USAGE[user_id]:
            del _COMMAND_USAGE[user_id]


def general_chat_only(func):
    @functools.wraps(func)
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        if update.effective_message.message_thread_id is not None:
            return None
        return await func(update, context, *args, **kwargs)

    return wrapper
