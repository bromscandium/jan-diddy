from app.core.llm import llm_settings
from app.persona.client.base import request


async def rewrite(seed: str, timeout: float = 20.0) -> str | None:
    payload = {"messages": [{"username": "jan", "text": seed}], "mode": "rewrite"}
    return await request("POST", "/v1/generate-reply", timeout=timeout, json=payload, key="reply")


async def generate(
    messages: list[dict],
    chat_id: int,
    thread_id: int | None,
    mode: str = "spontaneous",
    target: dict | None = None,
) -> str | None:
    payload = {
        "messages": messages,
        "chat_id": chat_id,
        "thread_id": thread_id,
        "mode": mode,
        "target": target,
    }
    return await request(
        "POST", "/v1/generate-reply", timeout=llm_settings.PERSONA_ENGINE_TIMEOUT, json=payload, key="reply", retries=2
    )
