from datetime import datetime, timedelta

from app.core.bot import bot_settings
from app.core.http import HttpClient

URL = "http://api.openweathermap.org/data/2.5/weather?q=Kosice&appid={key}&units=metric&lang=sk"


def _format(data: dict) -> str:
    m = data["main"]
    sunrise = (datetime.fromtimestamp(data["sys"]["sunrise"]) + timedelta(hours=2)).strftime("%H:%M")
    sunset = (datetime.fromtimestamp(data["sys"]["sunset"]) + timedelta(hours=2)).strftime("%H:%M")
    return (
        f"Počasie v Košiciach:\n"
        f"{data['weather'][0]['description'].capitalize()}\n"
        f"Teplota: {m['temp']}°C (pocitovo {m['feels_like']}°C)\n"
        f"Vlhkosť: {m['humidity']}%\n"
        f"Vietor: {data['wind']['speed']} m/s\n"
        f"Oblačnosť: {data['clouds']['all']}%\n\n"
        f"Východ: {sunrise}, Západ: {sunset}"
    )


async def fetch_weather() -> str | None:
    if not HttpClient.session:
        return None
    async with HttpClient.session.get(URL.format(key=bot_settings.WEATHER_API_KEY)) as resp:
        if resp.status != 200:
            return None
        data = await resp.json()
    return _format(data)
