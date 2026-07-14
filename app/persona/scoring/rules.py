from app.persona import lexicon

ENGAGEMENT_EMOJI = {"😂", "🤣", "🔥", "❤", "❤️", "👍", "👏", "💯", "🫡"}
NEGATIVE_EMOJI = {"🤮", "🤢", "🥱"}
AMBIGUOUS_EMOJI = {"🤡", "👎", "💩"}


def _channel(text: str, group: str) -> int:
    return lexicon.count(text, "scoring", group)


def _emoji(text: str, chars: set[str]) -> int:
    return sum(text.count(c) for c in chars)


def is_quality_mark(text: str) -> bool:
    return text.strip().lower().startswith("/q")


def has_signal(text: str) -> bool:
    if is_quality_mark(text):
        return True
    return bool(
        _channel(text, "laugh")
        or _channel(text, "approval")
        or _channel(text, "negative")
        or _channel(text, "ambiguous")
        or _emoji(text, ENGAGEMENT_EMOJI)
        or _emoji(text, NEGATIVE_EMOJI)
        or _emoji(text, AMBIGUOUS_EMOJI)
    )


def reply_score(text: str) -> int:
    if is_quality_mark(text):
        return 5
    laugh = _channel(text, "laugh") + _emoji(text, ENGAGEMENT_EMOJI)
    appr = _channel(text, "approval")
    neg = _channel(text, "negative") + _emoji(text, NEGATIVE_EMOJI)
    amb = _channel(text, "ambiguous") + _emoji(text, AMBIGUOUS_EMOJI)
    if laugh:
        return max(1, 2 + min(laugh, 3) + min(appr, 1) - min(neg, 2))
    if neg:
        return -(2 + min(neg, 2))
    if appr:
        return max(1, 1 + min(appr, 3))
    if amb:
        return -1
    return 0


def reaction_score(emoji: str) -> int:
    if emoji in ENGAGEMENT_EMOJI:
        return 3
    if emoji in NEGATIVE_EMOJI:
        return -3
    if emoji in AMBIGUOUS_EMOJI:
        return -1
    return 1
