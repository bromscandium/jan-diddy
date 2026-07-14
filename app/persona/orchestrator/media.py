import base64

from app.core.llm import llm_settings
from app.core.logger import logger
from app.persona import client


def media_label(msg) -> str | None:
    if msg.sticker:
        return f"[стікер {msg.sticker.emoji}]" if msg.sticker.emoji else "[стікер]"
    if msg.photo:
        return "[фото]"
    if msg.animation:
        return "[гіф]"
    if msg.voice:
        return "[голосове]"
    if msg.video or msg.video_note:
        return "[відео]"
    if msg.audio:
        return "[аудіо]"
    return None


async def photo_caption(msg, bot) -> str | None:
    photo = msg.photo[-1]
    if photo.file_size and photo.file_size > llm_settings.CAPTION_MAX_BYTES:
        return None
    try:
        f = await bot.get_file(photo.file_id)
        buf = await f.download_as_bytearray()
        return await client.caption(base64.b64encode(bytes(buf)).decode())
    except Exception as exc:
        logger.warning(f"photo caption failed: {exc}")
        return None


async def media_text(msg, bot) -> str | None:
    label = media_label(msg)
    if not label:
        return None
    if msg.photo and llm_settings.CAPTION_ENABLED:
        cap = await photo_caption(msg, bot)
        if cap:
            label = f"[фото: {cap}]"
    caption = (msg.caption or "").strip()
    has_link = any(e.type in ("url", "text_link") for e in (msg.caption_entities or []))
    if caption and not has_link and "http" not in caption.lower() and not caption.startswith("/"):
        return f"{label} {caption}"
    return label
