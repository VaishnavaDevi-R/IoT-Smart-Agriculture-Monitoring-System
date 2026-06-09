import json
import os

STATE_FILE = "data/farm_state.json"

DEFAULT_STATE = {
    "soil_moisture": 75.0,
    "water_level": 100.0,
    "pump_status": "OFF",
    "weather": "Sunny"
}


def load_state():

    if not os.path.exists(STATE_FILE):
        save_state(DEFAULT_STATE)
        return DEFAULT_STATE

    with open(STATE_FILE, "r") as file:
        return json.load(file)


def save_state(state):

    with open(STATE_FILE, "w") as file:
        json.dump(state, file, indent=4)