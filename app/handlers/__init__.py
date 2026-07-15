from telegram.ext import Application, CommandHandler, MessageHandler, MessageReactionHandler, filters

from app.community.handlers import admin, chat, events, fun, info
from app.persona.handlers import listener, reactions

admin_commands = {
    "mute": admin.mute,
    "unmute": admin.unmute,
    "ban": admin.ban,
    "unban": admin.unban,
    "warn": admin.warn,
    "unwarn": admin.unwarn,
    "listwarn": admin.listwarn,
}

info_commands = {
    "rules": info.rules,
    "moodle": info.moodle,
    "links": info.links,
    "scores": info.scores,
    "plan": info.plan,
    "maptuke": info.maptuke,
    "map5p": info.map5p,
    "studijne": info.studijne,
    "schedule": info.schedule,
    "invite": info.invite,
    "week": info.week,
}

fun_commands = {
    "predict": fun.predict,
    "joke": fun.joke,
    "weather": fun.weather,
    "chance": fun.chance,
}

chat_commands = {
    "start": chat.start,
}

all_commands = {**admin_commands, **info_commands, **fun_commands, **chat_commands}


def setup_handlers(app: Application) -> None:
    for command, handler in all_commands.items():
        app.add_handler(CommandHandler(command, handler))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fun.bro_monitor))
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE & ~filters.COMMAND, chat.start_message))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, events.welcome))
    app.add_handler(
        MessageHandler(
            (filters.ChatType.GROUP | filters.ChatType.SUPERGROUP) & filters.TEXT & ~filters.COMMAND,
            listener.listener,
        ),
        group=1,
    )
    media_filter = (
        filters.Sticker.ALL
        | filters.PHOTO
        | filters.ANIMATION
        | filters.VIDEO
        | filters.VIDEO_NOTE
        | filters.VOICE
        | filters.AUDIO
    )
    app.add_handler(
        MessageHandler((filters.ChatType.GROUP | filters.ChatType.SUPERGROUP) & media_filter, listener.media_listener),
        group=1,
    )
    app.add_handler(MessageReactionHandler(reactions.on_reaction), group=1)


__all__ = [
    "setup_handlers",
    "events",
    "chat",
]
