from app.persona.client.base import request


async def refresh_dossiers(user_ids: list[int]) -> None:
    await request("POST", "/v1/dossiers/refresh", timeout=15.0, json={"user_ids": user_ids}, key=None)
