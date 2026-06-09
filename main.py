from python_simulation.sensor_simulator import generate_sensor_data
from python_simulation.data_logger import save_data
from python_simulation.alert_system import check_alerts
from python_simulation.pump_controller import control_pump

sensor_data = generate_sensor_data()

pump_status = control_pump(sensor_data)

sensor_data["pump_status"] = pump_status

print("\n🌱 IoT Smart Agriculture Monitoring System")
print("=" * 50)

for key, value in sensor_data.items():
    print(f"{key}: {value}")

print("\n🚨 Alerts")
alerts = check_alerts(sensor_data)

if alerts:
    for alert in alerts:
        print(alert)
else:
    print("✅ No Alerts")

print(f"\n🚰 Pump Status: {pump_status}")

save_data(sensor_data)