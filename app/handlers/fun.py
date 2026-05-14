import random
from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import CallbackContext

from app.core.config import settings
from app.core.http import HttpClient
from app.services import jokes, predictions
from app.utils.decorators import general_chat_only, personal_limit


@personal_limit(12000)
async def bless(update: Update, context: CallbackContext):
    if not update.message or not update.message.text:
        return

    text = update.message.text
    if len(text.split()) < 2:
        await update.message.reply_text("Prosim, napiste v tomto formate: /bless VasTitul.")
        return

    new_title = " ".join(text.split()[1:])
    chat_admins = await context.bot.get_chat_administrators(chat_id=settings.CHAT_ID)
    user_is_admin = any(admin.user.id == update.message.from_user.id for admin in chat_admins)

    if not user_is_admin:
        await context.bot.promote_chat_member(
            chat_id=settings.CHAT_ID, user_id=update.message.from_user.id, can_post_messages=True, can_manage_chat=True
        )

    await context.bot.set_chat_administrator_custom_title(
        chat_id=settings.CHAT_ID, user_id=update.message.from_user.id, custom_title=new_title
    )
    await update.message.reply_text(f"Tvoj novy titul: {new_title}")


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
