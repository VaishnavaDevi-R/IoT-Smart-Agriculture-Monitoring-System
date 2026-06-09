from python_simulation.farm_state import (
    load_state,
    save_state
)


def control_pump(sensor_data):

    state = load_state()

    if (
        sensor_data["soil_moisture"] < 35
        and sensor_data["water_level"] > 15
    ):

        state["pump_status"] = "ON"

    else:

        state["pump_status"] = "OFF"

    save_state(state)

    return state["pump_status"]