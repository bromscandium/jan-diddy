from app.core.llm import llm_settings
from app.persona import client, state


async def maybe_refresh_dossiers(msg) -> None:
    if not llm_settings.DOSSIER_AUTO_REFRESH:
        return
    if not await state.bump_dossier(msg.chat_id, msg.message_thread_id, llm_settings.DOSSIER_REFRESH_EVERY):
        return
    ctx = await state.get_context(msg.chat_id, msg.message_thread_id)
    user_ids = list({m["user_id"] for m in ctx if m.get("user_id")})[:50]
    if user_ids:
        await client.refresh_dossiers(user_ids)
