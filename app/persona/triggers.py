import random
import time
from datetime import datetime
from zoneinfo import ZoneInfo

from app.core.bot import bot_settings
from app.core.llm import TrackConfig, TriggerConfig


def _local_hour() -> int:
    return datetime.now(ZoneInfo(bot_settings.TIMEZONE)).hour


def _in_hours(cfg: TriggerConfig) -> bool:
    start, end = cfg.active_hours
    return start <= _local_hour() < end


def should_prewarm(state: dict, cfg: TriggerConfig) -> bool:
    if not _in_hours(cfg):
        return False
    if state["prewarmed"]:
        return False
    now = time.time()
    return (
        state["count"] >= cfg.prewarm_messages
        and now - state["last_response_ts"] >= cfg.prewarm_minutes * 60
    )


def should_reply(track: TrackConfig, state: dict, cfg: TriggerConfig, bias: float = 1.0) -> bool:
    now = time.time()
    if not _in_hours(cfg):
        return False
    if now < state["cooldown_until"]:
        return False
    if state["count"] < track.min_messages:
        return False
    if now - state["last_response_ts"] < track.min_minutes * 60:
        return False
    return random.random() < min(1.0, track.probability * bias)
