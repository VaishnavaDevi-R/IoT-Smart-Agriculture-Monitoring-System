import csv
import os

FILE_PATH = "data/sensor_data.csv"


def save_data(sensor_data):

    headers = [
        "timestamp",
        "city",
        "weather",
        "temperature",
        "humidity",
        "wind_speed",
        "soil_moisture",
        "light_intensity",
        "water_level",
        "pump_status"
    ]

    file_exists = os.path.isfile(FILE_PATH)

    with open(FILE_PATH, mode="a", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=headers
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(sensor_data)

    print("✅ Data saved to CSV")