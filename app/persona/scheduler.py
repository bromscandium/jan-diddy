from datetime import time as dt_time
from zoneinfo import ZoneInfo

from telegram.ext import Application, CallbackContext

from app.core.bot import bot_settings
from app.core.llm import llm_settings
from app.core.logger import logger
from app.persona import client


async def _refresh_memory() -> None:
    try:
        await client.refresh_memory()
    except Exception as exc:
        logger.warning(f"memory refresh trigger failed: {exc!r}")


async def _memory_job(context: CallbackContext) -> None:
    await _refresh_memory()


async def schedule_memory(app: Application) -> None:
    if not llm_settings.MEMORY_AUTO_REFRESH:
        return
    await _refresh_memory()
    app.job_queue.run_daily(_memory_job, time=dt_time(0, 0, tzinfo=ZoneInfo(bot_settings.TIMEZONE)))
