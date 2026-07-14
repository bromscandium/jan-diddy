import httpx

from app.core.llm import llm_settings
from app.core.logger import logger


def _engine_headers() -> dict[str, str]:
    if llm_settings.PERSONA_ENGINE_SECRET:
        return {"X-Engine-Secret": llm_settings.PERSONA_ENGINE_SECRET}
    return {}


async def rewrite(seed: str, timeout: float = 20.0) -> str | None:
    url = f"{llm_settings.PERSONA_ENGINE_URL}/v1/generate-reply"
    payload = {"messages": [{"username": "jan", "text": seed}], "mode": "rewrite"}
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(url, json=payload, headers=_engine_headers())
            resp.raise_for_status()
            return (resp.json().get("reply", "") or "").strip() or None
    except Exception as exc:
        logger.warning(f"rewrite failed: {exc}")
        return None


async def caption(image_b64: str) -> str | None:
    url = f"{llm_settings.PERSONA_ENGINE_URL}/v1/caption"
    try:
        async with httpx.AsyncClient(timeout=llm_settings.CAPTION_TIMEOUT) as client:
            resp = await client.post(url, json={"image_b64": image_b64}, headers=_engine_headers())
            resp.raise_for_status()
            return (resp.json().get("caption") or "").strip() or None
    except Exception as exc:
        logger.warning(f"caption failed: {exc}")
        return None


async def prewarm() -> None:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.get(f"{llm_settings.PERSONA_ENGINE_URL}/health", headers=_engine_headers())
    except Exception as exc:
        logger.warning(f"prewarm failed: {exc}")


async def generate(
    messages: list[dict],
    chat_id: int,
    thread_id: int | None,
    mode: str = "spontaneous",
    target: dict | None = None,
) -> str | None:
    url = f"{llm_settings.PERSONA_ENGINE_URL}/v1/generate-reply"
    payload = {
        "messages": messages,
        "chat_id": chat_id,
        "thread_id": thread_id,
        "mode": mode,
        "target": target,
    }
    for attempt in range(2):
        try:
            async with httpx.AsyncClient(timeout=llm_settings.PERSONA_ENGINE_TIMEOUT) as client:
                resp = await client.post(url, json=payload, headers=_engine_headers())
                if resp.status_code == 502:
                    continue
                resp.raise_for_status()
                reply = resp.json().get("reply", "").strip()
                return reply or None
        except Exception as exc:
            logger.warning(f"engine call failed (attempt {attempt}): {exc}")
    return None
