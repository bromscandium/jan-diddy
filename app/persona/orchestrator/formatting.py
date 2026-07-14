import re

from app.core.llm import llm_settings
from app.persona.rendering import BURST_SEP, render_context

_JUNK = re.compile(r"^[\s▀-◿⬀-⯿�]+$")


def context_text(ctx: list[dict]) -> str:
    if llm_settings.PERSONA_FORMAT == "tagged":
        return render_context(ctx)
    return "\n".join(f"{m['username']}: {m['text']}" for m in ctx)


def format_outgoing(reply: str) -> str:
    parts = [p.strip() for p in reply.split(BURST_SEP)]
    parts = [p for p in parts if p and not _JUNK.match(p)]
    parts = parts[:3] or [reply.strip()]
    return " ".join(s + ("." if s[-1:].isalnum() else "") for s in parts)
