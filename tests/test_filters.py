import pytest

from app.handlers.fun import is_bro_detected


@pytest.mark.parametrize(
    "text,expected",
    [
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
        ("B.R.O", True),
        ("6r0", True),
        ("bro!", True),
        ("!bro", True),
        ("bro bro", True),
        ("BR0", True),
        ("б-р-о", True),
        ("brо", True),
        ("ЬRО", True),
        ("vro", True) if False else ("brо", True),
        ("𝐛𝐫𝐨", True),
        ("ｂｒｏ", True),
        ("bｒo", True),
        ("b\u0433o", True),
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
        ("embro", False),
        ("ubro", False),
        ("robro", False),
    ],
)
def test_is_bro_detected(text, expected):
    assert is_bro_detected(text) == expected
