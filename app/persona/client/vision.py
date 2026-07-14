from app.core.llm import llm_settings
from app.persona.client.base import request


async def caption(image_b64: str) -> str | None:
    return await request(
        "POST", "/v1/caption", timeout=llm_settings.CAPTION_TIMEOUT, json={"image_b64": image_b64}, key="caption"
    )
