BURST_SEP = "‖"


def speaker_label(from_id: str | None, display: str) -> str:
    return f"[{from_id or 'user0'}] {display}"


def relative_time(delta_seconds: int) -> str:
    if delta_seconds < 60:
        return "щойно"
    if delta_seconds < 3600:
        return "недавно"
    if delta_seconds < 86400:
        return "давно"
    return "дуже давно"


def gap_marker(delta_seconds: int) -> str:
    return "— велика пауза —"


def render_line(from_id: str | None, display: str, ts: int | None, anchor_ts: int | None, text: str) -> str:
    label = speaker_label(from_id, display)
    if ts and anchor_ts:
        return f"{label} · {relative_time(max(0, anchor_ts - ts))}: {text}"
    return f"{label}: {text}"


def render_context(messages: list[dict], gap_threshold_min: int = 30) -> str:
    anchor = max((m.get("ts") for m in messages if m.get("ts")), default=None)
    lines: list[str] = []
    prev: int | None = None
    for m in messages:
        ts = m.get("ts")
        if prev and ts and ts - prev >= gap_threshold_min * 60:
            lines.append(gap_marker(ts - prev))
        fid = f"user{m['user_id']}" if m.get("user_id") else None
        lines.append(render_line(fid, m.get("username", "anon"), ts, anchor, m.get("text", "")))
        if ts:
            prev = ts
    return "\n".join(lines)
