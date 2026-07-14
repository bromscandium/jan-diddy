from app.persona.client.base import request


async def prewarm() -> None:
    await request("GET", "/health", timeout=10.0)
