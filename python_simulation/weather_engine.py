import random


def get_weather():

    weather_options = [
        "Sunny",
        "Cloudy",
        "Rainy"
    ]

    weights = [0.5, 0.3, 0.2]

    return random.choices(
        weather_options,
        weights=weights,
        k=1
    )[0]