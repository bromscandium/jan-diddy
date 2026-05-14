from datetime import timedelta

from telegram import ChatPermissions, Update
from telegram.ext import CallbackContext

from app.core.config import settings
from app.services import warnings
from app.utils.decorators import admin_only


async def is_possible(update: Update, required_permission: str, use_grant_admins=False) -> bool:
    if not update.message:
        return False
    allowed_ids = settings.GRANT_ADMIN_IDS if use_grant_admins else settings.ADMIN_IDS

    if update.message.from_user.id not in allowed_ids:
        await update.message.reply_text("Ledači ako ty nemôžu používať tento príkaz.")
        return False

    user = update.message.reply_to_message.from_user

    if user is None:
        await update.message.reply_text("Ledač neexistuje.")
        return False

    if user.id in settings.ADMIN_IDS:
        await update.message.reply_text(f"{user.full_name} je hlavny administrátor.")
        return False

    chat_administrators = await update.effective_chat.get_administrators()

    for admin in chat_administrators:
        if admin.user.id == update.message.from_user.id:
            if getattr(admin, required_permission, False):
                return True
            else:
                await update.message.reply_text(f"{admin.user.full_name} nema tejto moznosti.")
                return False

    return True


@admin_only
async def mute(update: Update, context: CallbackContext) -> None:
    if not await is_possible(update, "can_restrict_members"):
        return
    user = update.message.reply_to_message.from_user
    duration = int(context.args[0]) if len(context.args) > 0 else 0
    if duration < 59:
        duration = 60
    until_date = None if duration == 0 else update.message.date + timedelta(seconds=duration)
    await context.bot.restrict_chat_member(
        chat_id=update.effective_chat.id,
        user_id=user.id,
        permissions=ChatPermissions.no_permissions(),
        until_date=until_date,
    )
    await update.message.reply_text(f"Ledač {user.full_name} zaspal.")


@admin_only
async def unmute(update: Update, context: CallbackContext) -> None:
    if not await is_possible(update, "can_restrict_members"):
        return

    user = update.message.reply_to_message.from_user
    await context.bot.restrict_chat_member(
        chat_id=update.effective_chat.id, user_id=user.id, permissions=ChatPermissions.all_permissions()
    )

    await update.message.reply_text(f"Ledač {user.full_name} sa zobudil.")


@admin_only
async def ban(update: Update, context: CallbackContext) -> None:
    if not await is_possible(update, "can_restrict_members"):
        return

    user = update.message.reply_to_message.from_user

    await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=user.id)
    await update.message.reply_text(f"Ledač {user.full_name} zaspal navždy.")


@admin_only
async def unban(update: Update, context: CallbackContext) -> None:
    if not await is_possible(update, "can_restrict_members"):
        return

    user = update.message.reply_to_message.from_user

    await context.bot.unban_chat_member(chat_id=update.effective_chat.id, user_id=user.id)
    await update.message.reply_text(f"Ledač {user.full_name} sa môže zobudiť.")


async def listwarn(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
    else:
        user = update.message.from_user

    user_warnings = await warnings.read_all_warnings_by_user_id(user.id)

    if not user_warnings:
        await update.message.reply_text("Tento ledač nemá žiadne varovania.")
    else:
        reasons = "\n".join([f"{i + 1}. {w.reason}" for i, w in enumerate(user_warnings)])
        await update.message.reply_text(f"{user.full_name} má {len(user_warnings)} varovania:\n\n{reasons}")


@admin_only
async def warn(update: Update, context: CallbackContext) -> None:
    if not await is_possible(update, "can_restrict_members"):
        return

    user = update.message.reply_to_message.from_user
    reason = " ".join(context.args) if context.args else "Bez dôvodu"

    await warnings.create_warning(user.id, reason)
    user_warnings = await warnings.read_all_warnings_by_user_id(user.id)
    warnings_count = len(user_warnings)

    if warnings_count >= 3:
        until_date = update.message.date + timedelta(days=2)
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user.id,
            permissions=ChatPermissions.no_permissions(),
            until_date=until_date,
        )
        await warnings.delete_all_warnings_by_user_id(user.id)
        await update.message.reply_text(f"{user.full_name} dostal {warnings_count} varovaní a bude spat 2 dni.")
    else:
        await update.message.reply_text(f"{user.full_name} dostal varovanie. Teraz má {warnings_count}.")


@admin_only
async def unwarn(update: Update, context: CallbackContext) -> None:
    if not await is_possible(update, "can_restrict_members"):
        return
    user = update.message.reply_to_message.from_user
    await warnings.delete_all_warnings_by_user_id(user.id)
    await update.message.reply_text(f"Všetky varovania boli vymazané z ledača {user.full_name}.")


@admin_only
async def reset_warn(update: Update, context: CallbackContext) -> None:
    if not getattr(await update.effective_chat.get_member(update.effective_user.id), "can_restrict_members", False):
        await update.message.reply_text(f"{update.effective_user.full_name} nema tejto moznosti.")
        return

    await warnings.delete_all_warnings()
    await context.bot.send_message(chat_id=settings.CHAT_ID, text="Všetky varovania boli automaticky resetované!")
