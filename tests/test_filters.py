import pytest
from app.handlers.fun import is_bro_detected

@pytest.mark.parametrize("text,expected", [
    # Positive cases (should detect)
    ("бро", True),
    ("bro", True),
    ("B R O", True),
    ("б р о", True),
    ("б.р.о", True),
    ("br0", True),
    ("6ro", True),
    ("БРО", True),
    ("brrooo", True),
    ("hey bro!", True),
    ("ти шо, бро?", True),
    ("b_r_o", True),
    
    # Negative cases (should NOT detect)
    ("dobro", False),
    ("добро", False),
    ("striebro", False),
    ("obrovský", False),
    ("бронежилет", False),
    ("амброзія", False),
    ("бра", False),
    ("бор", False),
    ("брокер", False),
    ("бродяга", False),
])
def test_is_bro_detected(text, expected):
    assert is_bro_detected(text) == expected
