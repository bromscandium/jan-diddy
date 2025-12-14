from app.handlers import chat, events, admin, info, fun

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
    "bless": fun.bless,
}

chat_commands = {
    "start": chat.start,
}

all_commands = {**admin_commands, **info_commands, **fun_commands, **chat_commands}

__all__ = [
    'all_commands',
    'events',
    'chat',
]
