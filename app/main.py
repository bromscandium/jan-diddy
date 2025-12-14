from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from app.core.config import bot_settings
from app.db.postgres import connect_db, close_db
from app.handlers import chat, events, all_commands


def main() -> None:
    bot = (
        ApplicationBuilder()
        .token(bot_settings.telegram_api_key)
        .post_init(connect_db)
        .post_shutdown(close_db)
        .build()
    )

    for command, handler in all_commands.items():
        bot.add_handler(CommandHandler(command, handler))

    bot.add_handler(MessageHandler(filters.ChatType.PRIVATE & ~filters.COMMAND, chat.start_message))
    bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, events.welcome))
    bot.add_handler(
        MessageHandler((filters.ChatType.GROUP | filters.ChatType.SUPERGROUP) & ~filters.COMMAND, events.reaction))

    print("Starting Telegram Bot...")
    bot.run_polling(drop_pending_updates=True)


if __name__ == '__main__':
    main()
