from datetime import datetime
import random

from python_simulation.farm_state import (
    load_state,
    save_state
)

from python_simulation.weather_service import (
    get_live_weather
)


def generate_sensor_data():

    state = load_state()

    weather_data = get_live_weather()

    weather = weather_data["weather"]
    temperature = weather_data["temperature"]
    humidity = weather_data["humidity"]

    soil_moisture = state["soil_moisture"]
    water_level = state["water_level"]
    pump_status = state["pump_status"]

    # Soil behaviour based on real weather

    if weather in ["Clear", "Sunny"]:

        soil_moisture -= random.uniform(1.0, 2.0)

    elif weather in ["Clouds", "Cloudy"]:

        soil_moisture -= random.uniform(0.3, 1.0)

    elif weather in ["Rain", "Drizzle", "Thunderstorm"]:

        soil_moisture += random.uniform(3, 8)

    # Pump irrigation

    if pump_status == "ON":

        soil_moisture += random.uniform(3, 6)

        water_level -= random.uniform(1, 3)

    soil_moisture = max(0, min(100, soil_moisture))
    water_level = max(0, min(100, water_level))

    # Light estimation

    current_hour = datetime.now().hour

    if 6 <= current_hour <= 18:

        if weather in ["Clear", "Sunny"]:
            light_intensity = random.randint(800, 1000)

        elif weather in ["Clouds", "Cloudy"]:
            light_intensity = random.randint(400, 700)

        else:
            light_intensity = random.randint(100, 400)

    else:

        light_intensity = random.randint(0, 100)

    state["soil_moisture"] = round(soil_moisture, 2)
    state["water_level"] = round(water_level, 2)

    save_state(state)

    return {
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "city": weather_data["city"],
        "weather": weather,
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": weather_data["wind_speed"],
        "soil_moisture": round(soil_moisture, 2),
        "light_intensity": light_intensity,
        "water_level": round(water_level, 2)
    }