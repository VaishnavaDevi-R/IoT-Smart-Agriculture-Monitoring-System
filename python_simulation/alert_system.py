def check_alerts(sensor_data):

    alerts = []

    if sensor_data["soil_moisture"] < 30:
        alerts.append("⚠ Soil Moisture Critically Low")

    if sensor_data["temperature"] > 40:
        alerts.append("⚠ High Temperature Warning")

    if sensor_data["water_level"] < 20:
        alerts.append("⚠ Water Tank Running Low")

    if sensor_data["weather"] == "Rainy":
        alerts.append("🌧 Rain Detected - Irrigation Not Required")

    return alerts