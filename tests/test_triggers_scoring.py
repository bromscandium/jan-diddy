import time

from app.core.llm import DEBUG, PROD
from app.persona.services import scoring, triggers


def _state(**kw) -> dict:
    base = {"count": 100, "last_response_ts": 0.0, "cooldown_until": 0.0, "prewarmed": False}
    base.update(kw)
    return base


def test_should_reply_fires_when_conditions_met():
    assert triggers.should_reply(DEBUG.addressed, _state(), DEBUG) is True


def test_should_reply_blocked_by_count():
    assert triggers.should_reply(DEBUG.spontaneous, _state(count=0), DEBUG) is False


def test_should_reply_blocked_by_cooldown():
    assert triggers.should_reply(DEBUG.addressed, _state(cooldown_until=time.time() + 9999), DEBUG) is False


def test_zero_probability_never_fires():
    zero = PROD.spontaneous.__class__(min_messages=0, min_minutes=0, probability=0.0, cooldown_minutes=0)
    assert triggers.should_reply(zero, _state(), DEBUG) is False


def test_keyword_score_positive_and_negative():
    assert scoring.keyword_score("ахаха жесть") > 0
    assert scoring.keyword_score("це база") > 0
    assert scoring.keyword_score("ну це хуйня") < 0
    assert scoring.keyword_score("доброго ранку") == 0


def test_keyword_detected_inside_word():
    assert scoring.keyword_score("ти ахуєнно зробив") > 0
    assert scoring.keyword_score("повна хуйня вийшла") < 0


def test_reaction_weights_grade():
    assert scoring.REACTION_WEIGHTS["😂"] > scoring.REACTION_WEIGHTS["👍"]
    assert scoring.REACTION_WEIGHTS["👎"] < 0
    assert scoring.REACTION_WEIGHTS["🤮"] < 0
    assert "💀" not in scoring.REACTION_WEIGHTS
