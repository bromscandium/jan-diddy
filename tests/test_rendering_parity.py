from app.persona.services.rendering import render_context

EXPECTED = (
    "[user1] Аня · 1 год тому: привіт\n"
    "[user2] Боб · 50 хв тому: як діла\n"
    "— пауза 50 хв —\n"
    "[user1] Аня · щойно: нормас"
)


def test_render_context_matches_shared_format():
    msgs = [
        {"ts": 1000, "user_id": 1, "username": "Аня", "text": "привіт"},
        {"ts": 2000, "user_id": 2, "username": "Боб", "text": "як діла"},
        {"ts": 5000, "user_id": 1, "username": "Аня", "text": "нормас"},
    ]
    assert render_context(msgs) == EXPECTED
