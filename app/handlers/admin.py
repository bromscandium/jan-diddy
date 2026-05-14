from datetime import timedelta

from telegram import ChatPermissions, Update
from telegram.ext import CallbackContext

from app.services import warnings
from app.utils.decorators import admin_limit


@admin_limit
async def mute(update: Update, context: CallbackContext) -> None:
    user = update.message.reply_to_message.from_user
    duration = int(context.args[0]) if len(context.args) > 0 else 0
    if duration < 59:
        duration = 60
    until_date = None if duration == 0 else update.message.date + timedelta(seconds=duration)
    
    try:
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user.id,
            permissions=ChatPermissions.no_permissions(),
            until_date=until_date,
        )
        await update.message.reply_text(f"Ledač {user.full_name} bol uspaný.")
    except Exception:
        await update.message.reply_text("Nemám dostatočné oprávnenia na uspanie tohto ledača.")


@admin_limit
async def unmute(update: Update, context: CallbackContext) -> None:
    user = update.message.reply_to_message.from_user
    try:
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id, user_id=user.id, permissions=ChatPermissions.all_permissions()
        )
        await update.message.reply_text(f"Ledač {user.full_name} bol prebudený.")
    except Exception:
        await update.message.reply_text("Nemám oprávnenia na prebudenie tohto ledača.")


@admin_limit
async def ban(update: Update, context: CallbackContext) -> None:
    user = update.message.reply_to_message.from_user
    try:
        await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=user.id)
        await update.message.reply_text(f"Ledač {user.full_name} bol uspaný navždy.")
    except Exception:
        await update.message.reply_text("Nemám oprávnenia na zabanovanie tohto ledača.")


@admin_limit
async def unban(update: Update, context: CallbackContext) -> None:
    user = update.message.reply_to_message.from_user
    try:
        await context.bot.unban_chat_member(chat_id=update.effective_chat.id, user_id=user.id)
        await update.message.reply_text(f"Ledač {user.full_name} sa môže vrátiť.")
    except Exception:
        await update.message.reply_text("Nemám oprávnenia na odbanovanie tohto ledača.")


@admin_limit
async def warn(update: Update, context: CallbackContext) -> None:
    user = update.message.reply_to_message.from_user
    reason = " ".join(context.args) if context.args else "Bez udania dôvodu"

    await warnings.create_warning(user.id, reason)
    user_warnings = await warnings.read_all_warnings_by_user_id(user.id)
    warnings_count = len(user_warnings)

    if warnings_count >= 3:
        until_date = update.message.date + timedelta(days=2)
        try:
            await context.bot.restrict_chat_member(
                chat_id=update.effective_chat.id,
                user_id=user.id,
                permissions=ChatPermissions.no_permissions(),
                until_date=until_date,
            )
            await warnings.delete_all_warnings_by_user_id(user.id)
            await update.message.reply_text(
                f"Ledač {user.full_name} nazbieral {warnings_count} varovania a bude spať 2 dni."
            )
        except Exception:
            await update.message.reply_text(f"Ledač {user.full_name} má 3 varovania, ale nemôžem ho obmedziť.")
    else:
        await update.message.reply_text(f"Ledač {user.full_name} dostal varovanie. Aktuálny počet: {warnings_count}.")


@admin_limit
async def unwarn(update: Update, context: CallbackContext) -> None:
    user = update.message.reply_to_message.from_user
    await warnings.delete_all_warnings_by_user_id(user.id)
    await update.message.reply_text(f"Všetky varovania ledača {user.full_name} boli zmazané.")


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
        await update.message.reply_text(f"Ledač {user.full_name} má {len(user_warnings)} varovania:\n\n{reasons}")