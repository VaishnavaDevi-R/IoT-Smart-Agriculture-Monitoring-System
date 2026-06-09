import os
import requests

try:
    import streamlit as st

    api_key = st.secrets["OPENWEATHER_API_KEY"]
    city = st.secrets["CITY"]

except Exception:

    from dotenv import load_dotenv

    load_dotenv()

    api_key = os.getenv("OPENWEATHER_API_KEY")
    city = os.getenv("CITY", "Chennai")


def get_live_weather():

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