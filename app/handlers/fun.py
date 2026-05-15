import random
import re
import unicodedata
from datetime import datetime, timedelta

from confusables import normalize as confusable_normalize
from telegram import Update
from telegram.ext import CallbackContext

from app.core.config import settings
from app.core.http import HttpClient
from app.services import jokes, predictions
from app.utils.decorators import general_chat_limit, personal_limit

# Evian, big brother is watching you

MULTI_CHAR_HOMOGLYPHS = {
    "()": "o",
    "[]": "o",
    "{}": "o",
    "<>": "o",
    "( )": "o",
    "[ ]": "o",
    "{ }": "o",
    "{)": "o",
    "(}": "o",
    "[)": "o",
    "(]": "o",
    "[ )": "o",
    "( ]": "o",
    "(.)": "o",
    "[.]": "o",
    "{.}": "o",
    "|3": "b",
    "13": "b",
    "l3": "b",
    "I3": "b",
    "/3": "b",
    "\\3": "b",
    "|)": "b",
    "|>": "b",
    "|]": "b",
    "|8": "b",
    "|S": "b",
    "|2": "r",
    "l2": "r",
}

HOMOGLYPHS = {
    "б": "b",
    "Б": "b",
    "В": "b",
    "в": "b",
    "Ь": "b",
    "ь": "b",
    "ъ": "b",
    "Ъ": "b",
    "ѣ": "b",
    "Ѣ": "b",
    "ћ": "b",
    "ђ": "b",
    "v": "b",
    "V": "b",
    "w": "b",
    "W": "b",
    "þ": "b",
    "Þ": "b",
    "ß": "b",
    "6": "b",
    "8": "b",
    "🇧": "b",
    "🅱": "b",
    "🐝": "b",
    "𝕓": "b",
    "𝓫": "b",
    "𝔟": "b",
    "p": "r",
    "P": "r",
    "р": "r",
    "Р": "r",
    "г": "r",
    "Г": "r",
    "я": "r",
    "Я": "r",
    "२": "r",
    "ρ": "r",
    "Ρ": "r",
    "ɹ": "r",
    "®": "r",
    "🇷": "r",
    "🅿": "r",
    "𝕣": "r",
    "𝓻": "r",
    "𝔯": "r",
    "о": "o",
    "О": "o",
    "0": "o",
    "ο": "o",
    "Ο": "o",
    "ø": "o",
    "Ø": "o",
    "θ": "o",
    "Θ": "o",
    "ѻ": "o",
    "ѳ": "o",
    "Ѳ": "o",
    "u": "o",
    "U": "o",
    "@": "o",
    "Q": "o",
    "⭕": "o",
    "🇴": "o",
    "🅾": "o",
    "🔴": "o",
    "🔵": "o",
    "⚪": "o",
    "⚫": "o",
    "🟡": "o",
    "🟢": "o",
    "🟣": "o",
    "🟤": "o",
    "🔘": "o",
    "🌕": "o",
    "⚽": "o",
    "🍊": "o",
    "𝕠": "o",
    "𝓸": "o",
    "𝔬": "o",
    "Ⓜ": "m",
}


def _normalize(text: str) -> str:
    if "\u202e" in text:
        parts = text.split("\u202e")
        text = parts[0] + "".join(p[::-1] for p in parts[1:])

    text = re.sub(r"[\u200b-\u200f\u202a-\u202d\u2060-\u206f\ufeff\u00ad]", "", text)
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = unicodedata.normalize("NFKC", text)

    for multi, replacement in MULTI_CHAR_HOMOGLYPHS.items():
        text = text.replace(multi, replacement)

    result = []
    for ch in text:
        mapped = HOMOGLYPHS.get(ch)
        result.append(mapped if mapped else ch)
    return "".join(result).lower()


def is_bro_detected(text: str) -> bool:
    if not text:
        return False

    def check_logic(n: str) -> bool:
        for raw_token in re.split(r"[\s,!?;:]+", n):
            if not raw_token:
                continue
            pure = "".join(c for c in raw_token if c.isalpha())
            if re.fullmatch(r"b+r+o+", pure):
                return True
        if re.search(r"(?<![^\W_])b+[\W_]*r+[\W_]*o+(?![^\W_])", n):
            return True
        return False

    if check_logic(_normalize(text)):
        return True

    try:
        variants = confusable_normalize(text) or []
        for v in variants:
            if v != text and "'" not in v and check_logic(_normalize(v)):
                return True
    except Exception:
        pass
    return False


async def bro_monitor(update: Update, context: CallbackContext):
    if not update.message or not update.message.text:
        return
    if update.effective_user.id not in settings.BANNED_BY_ID:
        return
    if is_bro_detected(update.message.text):
        await update.message.delete()


@general_chat_limit
@personal_limit(61)
async def predict(update: Update, context: CallbackContext):
    if not update.message:
        return
    await update.message.reply_text(
        f"Dnes máš takéto predpovedanie, {update.effective_user.full_name}:\n"
        f"{await predictions.read_random_prediction()}"
    )


@general_chat_limit
@personal_limit(121)
async def joke(update: Update, context: CallbackContext):
    if not update.message:
        return
    await update.message.reply_text(
        f"Počúvaj tento žart, {update.effective_user.full_name}:\n{await jokes.read_random_joke()}"
    )


@general_chat_limit
@personal_limit(61)
async def chance(update: Update, context):
    if not update.message:
        return
    text = update.message.text or ""
    parts = text.split(maxsplit=1)
    query = parts[1].strip() if len(parts) > 1 else ""
    num = random.randint(0, 100)
    if query:
        await update.message.reply_text(f"Šanca pre „{query}“: {num}%")
    else:
        await update.message.reply_text(f"Šanca byť hetero: {num}%")


@general_chat_limit
@personal_limit(121)
async def weather(update: Update, context: CallbackContext):
    if not update.message:
        return
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?q=Kosice&appid={settings.WEATHER_API_KEY}&units=metric&lang=sk"
    )
    if not HttpClient.session:
        await update.message.reply_text("Service temporarily unavailable.")
        return
    async with HttpClient.session.get(url) as resp:
        if resp.status != 200:
            await update.message.reply_text("Nepodarilo sa начітать počasie. Skús nesкôr.")
            return
        data = await resp.json()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"].capitalize()
        humidity = data["main"]["humidity"]
        sunrise = (datetime.fromtimestamp(data["sys"]["sunrise"]) + timedelta(hours=2)).strftime("%H:%M")
        sunset = (datetime.fromtimestamp(data["sys"]["sunset"]) + timedelta(hours=2)).strftime("%H:%M")
        wind = data["wind"]["speed"]
        clouds = data["clouds"]["all"]
        msg = (
            f"Počasie v Košiciach:\n"
            f"{description}\n"
            f"Teplota: {temp}°C (pocitovo {feels_like}°C)\n"
            f"Vlhkosť: {humidity}%\n"
            f"Vietor: {wind} m/s\n"
            f"Oblaчnosť: {clouds}%\n\n"
            f"Východ: {sunrise}, Západ: {sunset}"
        )
        await update.message.reply_text(msg)
