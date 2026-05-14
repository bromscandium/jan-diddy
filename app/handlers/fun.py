import random
import re
from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import CallbackContext

from app.core.config import settings
from app.core.http import HttpClient
from app.services import jokes, predictions
from app.utils.decorators import general_chat_only, personal_limit


def is_bro_detected(text: str) -> bool:
    if not text:
        return False
    n = text.lower()
    n = n.replace("0", "o").replace("6", "b").replace("p", "r")
    trans = {"b": "б", "r": "р", "o": "о"}
    for l, c in trans.items():
        n = n.replace(l, c)
    n = re.sub(r"[^а-яё]", "", n)
    return "бро" in n


async def bro_monitor(update: Update, context: CallbackContext):
    if not update.message or not update.message.text:
        return
    if update.effective_user.id not in settings.BANNED_BY_ID:
        return
    if is_bro_detected(update.message.text):
        await update.message.delete()

@general_chat_only
@personal_limit(61)
async def predict(update: Update, context: CallbackContext):
    if not update.message:
        return
    await update.message.reply_text(
        f"Dnes máš takéto predpovedanie, {update.effective_user.full_name}:\n"
        f"{await predictions.read_random_prediction()}"
    )


@general_chat_only
@personal_limit(121)
async def joke(update: Update, context: CallbackContext):
    if not update.message:
        return
    await update.message.reply_text(
        f"Počúvaj tento žart, {update.effective_user.full_name}:\n{await jokes.read_random_joke()}"
    )


@general_chat_only
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


@general_chat_only
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
