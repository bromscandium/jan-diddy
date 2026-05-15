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

HOMOGLYPHS = {
    "б": "b",
    "Б": "b",
    "В": "b",
    "в": "b",
    "ß": "b",
    "6": "b",
    "р": "r",
    "Р": "r",
    "ρ": "r",
    "Ρ": "r",
    "о": "o",
    "О": "o",
    "0": "o",
    "ο": "o",
    "Ο": "o",
    "ø": "o",
    "Ø": "o",
    "@": "o",
    "Q": "o",
}

_WORD_CHARS = re.compile(r"[^\W]", re.UNICODE)


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    result = []
    for ch in text:
        mapped = HOMOGLYPHS.get(ch)
        if mapped:
            result.append(mapped)
        elif ch.isalpha() and ord(ch) > 127:
            result.append("x")
        else:
            result.append(ch)
    return "".join(result).lower()


def is_bro_detected(text: str) -> bool:
    if not text:
        return False

    pattern = r"(?<![a-z0-9])b+[\W_]*r+[\W_]*o+(?![a-z0-9])"

    variants = confusable_normalize(text) or []
    for v in [text] + variants:
        if re.search(pattern, _normalize(v)):
            return True
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
            await update.message.reply_text("Nepodarilo sa naчітать počasie. Skús neskôr.")
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
            f"Oblačnosť: {clouds}%\n\n"
            f"Východ: {sunrise}, Západ: {sunset}"
        )
        await update.message.reply_text(msg)
