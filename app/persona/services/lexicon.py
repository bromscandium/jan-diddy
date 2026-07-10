import json
import re
from functools import cache, lru_cache
from pathlib import Path

_PATH = Path(__file__).with_name("lexicon.json")


@lru_cache(maxsize=1)
def _data() -> dict:
    with open(_PATH, encoding="utf-8") as f:
        return json.load(f)


def _compile(stem: str) -> re.Pattern:
    if stem.startswith("=") and len(stem) > 1:
        return re.compile(r"\b" + re.escape(stem[1:]) + r"\b")
    body = re.escape(stem)
    if re.match(r"\w", stem, re.UNICODE):
        return re.compile(r"\b" + body)
    return re.compile(body)


@cache
def _patterns(category: str, group: str) -> tuple[re.Pattern, ...]:
    return tuple(_compile(s) for s in _data()[category][group])


def matches(text: str, category: str, group: str) -> bool:
    low = text.lower()
    return any(p.search(low) for p in _patterns(category, group))


def count(text: str, category: str, group: str) -> int:
    low = text.lower()
    return sum(1 for p in _patterns(category, group) if p.search(low))


def first_match(text: str, category: str, default: str) -> str:
    low = text.lower()
    for group in _data()[category]:
        if any(p.search(low) for p in _patterns(category, group)):
            return group
    return default
