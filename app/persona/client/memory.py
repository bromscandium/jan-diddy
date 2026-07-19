from app.persona.client.base import request


async def refresh_memory() -> None:
    await request("POST", "/v1/memory/refresh", timeout=15.0, json={}, key=None)
