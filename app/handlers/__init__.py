from telegram.ext import Application, CommandHandler, MessageHandler, filters

from app.handlers import admin, chat, events, fun, info

admin_commands = {
    "mute": admin.mute,
    "unmute": admin.unmute,
    "ban": admin.ban,
    "unban": admin.unban,
    "warn": admin.warn,
    "unwarn": admin.unwarn,
    "listwarn": admin.listwarn,
    "resetwarn": admin.reset_warn,
}

info_commands = {
    "rules": info.rules,
    "moodle": info.moodle,
    "links": info.links,
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
        MessageHandler((filters.ChatType.GROUP | filters.ChatType.SUPERGROUP) & ~filters.COMMAND, events.reaction))

__all__ = [
    'setup_handlers',
    'events',
    'chat',
]
