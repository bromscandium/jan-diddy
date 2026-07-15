from app.core.llm import llm_settings
from app.persona.client.base import request


async def react(messages: list[dict], chat_id: int | None = None) -> str | None:
    return await request(
        "POST",
        "/v1/react",
        timeout=llm_settings.PERSONA_ENGINE_TIMEOUT,
        json={"messages": messages, "chat_id": chat_id},
        key="emoji",
    )
