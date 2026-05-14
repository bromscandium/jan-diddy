import functools
import time

from telegram import Update
from telegram.ext import CallbackContext

from app.core.config import settings

# NOTE: These limits are stored in memory and will reset upon bot restart (e.g., Railway redeploy).
_USER_LAST_CALLED = {}
_COMMAND_USAGE = {}


def admin_limit(func):
    @functools.wraps(func)
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        if not update.message or not update.effective_user:
            return

        member = await update.effective_chat.get_member(update.effective_user.id)
        if member.status not in ["administrator", "creator"] or not member.can_restrict_members:
            await update.message.reply_text("Ledači ako ty nemôžu používať tento príkaz.")

        if not update.message.reply_to_message:
            await update.message.reply_text("Vyskytla sa chyba pri šukaní ledača.")
            return

        target_user = update.message.reply_to_message.from_user
        if target_user and target_user.id in settings.ADMIN_IDS:
            await update.message.reply_text(f"{target_user.full_name} je hlavný administrátor.")
            return

        return await func(update, context, *args, **kwargs)

    return wrapper



def personal_limit(seconds: int):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
            user_id = update.effective_user.id
            key = (user_id, func.__name__)
            now = time.time()
            if now - _USER_LAST_CALLED.get(key, 0) < seconds:
                return
            _USER_LAST_CALLED[key] = now
            return await func(update, context, *args, **kwargs)

        return wrapper

    return decorator


def group_limit(func):
    @functools.wraps(func)
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = update.effective_user.id
        cmd = func.__name__

        user_usage = _COMMAND_USAGE.setdefault(user_id, {})
        if user_usage.get(cmd, 0) >= 2:
            return

        user_usage[cmd] = user_usage.get(cmd, 0) + 1
        context.job_queue.run_once(_reset_usage, 300, data=(user_id, cmd))

        return await func(update, context, *args, **kwargs)

    return wrapper


def general_chat_only(func):
    @functools.wraps(func)
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        if update.effective_message.message_thread_id is not None:
            return
        return await func(update, context, *args, **kwargs)

    return wrapper


async def _reset_usage(context: CallbackContext):
    user_id, cmd = context.job.data
    if user_id in _COMMAND_USAGE and cmd in _COMMAND_USAGE[user_id]:
        _COMMAND_USAGE[user_id][cmd] -= 1
        if _COMMAND_USAGE[user_id][cmd] <= 0:
            del _COMMAND_USAGE[user_id][cmd]
        if not _COMMAND_USAGE[user_id]:
            del _COMMAND_USAGE[user_id]
