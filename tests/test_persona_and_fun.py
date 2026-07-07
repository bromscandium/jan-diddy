from unittest.mock import AsyncMock, MagicMock

from app.community.handlers.fun import joke, predict, random_reply


async def test_random_reply_fills_template():
    async def fetch() -> str:
        return "XYZ"

    handler = random_reply("hi {name}: {text}", fetch)(lambda u, c: None)
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    update.effective_user.full_name = "Bob"

    await handler(update, None)

    update.message.reply_text.assert_awaited_once_with("hi Bob: XYZ")


async def test_random_reply_no_message_is_noop():
    async def fetch() -> str:
        return "XYZ"

    handler = random_reply("{name}: {text}", fetch)(lambda u, c: None)
    update = MagicMock()
    update.message = None

    await handler(update, None)


def test_predict_and_joke_keep_distinct_names():
    assert predict.__name__ == "predict"
    assert joke.__name__ == "joke"
    assert predict.__name__ != joke.__name__
