SCORING_WINDOW = 120
IGNORED_ACTIVITY_MIN = 3
PENDING_META_TTL = 7200


def meta_key(chat_id: int, bot_message_id: int) -> str:
    return f"jd:pendmeta:{chat_id}:{bot_message_id}"


def idx_key(chat_id: int, thread_id: int | None) -> str:
    return f"jd:pendidx:{chat_id}:{thread_id if thread_id is not None else 'none'}"


def lastbot_key(chat_id: int, thread_id: int | None) -> str:
    return f"jd:lastbot:{chat_id}:{thread_id if thread_id is not None else 'none'}"
