import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_live_weather():

    api_key = os.getenv("OPENWEATHER_API_KEY")
    city = os.getenv("CITY", "Chennai")

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}"
        f"&appid={api_key}"
        f"&units=metric"
    )

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        raise Exception(
            f"Weather API Error: {response.status_code}"
        )

    data = response.json()

    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["main"],
        "wind_speed": data["wind"]["speed"]
    }