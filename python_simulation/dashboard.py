import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Smart Agriculture Monitoring System",
    page_icon="🌱",
    layout="wide"
)

# Auto refresh every 10 seconds
st_autorefresh(
    interval=10000,
    key="dashboard_refresh"
)

# ==========================================
# LOAD DATA
# ==========================================

import os
import subprocess

csv_file = "data/sensor_data.csv"

if not os.path.exists(csv_file):

    st.info("🌱 Initializing farm data...")

    subprocess.run(
        ["python", "main.py"]
    )

try:
    df = pd.read_csv(csv_file)

except Exception:

    st.error(
        "Unable to load sensor data."
    )

    st.stop()

if df.empty:
    st.warning("⚠ No sensor data available.")
    st.stop()

latest = df.iloc[-1]

# ==========================================
# HEADER
# ==========================================

st.title("🌱 Smart Agriculture Monitoring System Pro")

st.markdown("""
### 🌾 Intelligent Farming Dashboard

Monitor live weather, irrigation status, soil moisture,
water levels, farm health, and smart recommendations
powered by real-time weather data.
""")

# ==========================================
# FARM HEALTH SCORE
# ==========================================

soil = float(latest["soil_moisture"])
water = float(latest["water_level"])
temp = float(latest["temperature"])

health_score = 100

if soil < 35:
    health_score -= 30

if water < 20:
    health_score -= 30

if temp > 40:
    health_score -= 20

health_score = max(0, health_score)

# ==========================================
# WEATHER SECTION
# ==========================================

st.subheader("🌤 Live Weather Conditions")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "🌡 Temperature",
    f"{latest['temperature']} °C"
)

c2.metric(
    "💧 Humidity",
    f"{latest['humidity']} %"
)

c3.metric(
    "☁ Weather",
    latest["weather"]
)

c4.metric(
    "🌬 Wind Speed",
    f"{latest['wind_speed']} m/s"
)

st.divider()

# ==========================================
# FARM STATUS
# ==========================================

st.subheader("🌱 Farm Status")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "🌱 Soil Moisture",
    f"{latest['soil_moisture']} %"
)

c2.metric(
    "🚰 Water Tank Level",
    f"{latest['water_level']} %"
)

c3.metric(
    "☀ Light Intensity",
    latest["light_intensity"]
)

c4.metric(
    "⚙ Pump Status",
    latest["pump_status"]
)

st.divider()

# ==========================================
# HEALTH SCORE
# ==========================================

st.subheader("💚 Farm Health Score")

st.progress(health_score / 100)

if health_score >= 80:
    st.success(
        f"Excellent Farm Condition ({health_score}%)"
    )

elif health_score >= 60:
    st.warning(
        f"Moderate Farm Condition ({health_score}%)"
    )

else:
    st.error(
        f"Critical Farm Condition ({health_score}%)"
    )

st.divider()

# ==========================================
# ALERT CENTER
# ==========================================

st.subheader("🚨 Alert Center")

alerts = []

if soil < 35:
    alerts.append("⚠ Soil Moisture Critically Low")

if water < 20:
    alerts.append("⚠ Water Tank Running Low")

if temp > 40:
    alerts.append("⚠ High Temperature Detected")

if latest["weather"] in [
    "Rain",
    "Drizzle",
    "Thunderstorm"
]:
    alerts.append("🌧 Rainfall Detected")

if alerts:

    for alert in alerts:
        st.warning(alert)

else:

    st.success("✅ No Active Alerts")

st.divider()

# ==========================================
# SMART RECOMMENDATION
# ==========================================

st.subheader("💡 Smart Recommendation")

if latest["weather"] in [
    "Rain",
    "Drizzle",
    "Thunderstorm"
]:
    st.info(
        "Rainfall detected. Irrigation not required."
    )

elif soil < 35:
    st.error(
        "Soil moisture is low. Start irrigation."
    )

else:
    st.success(
        "Farm conditions are healthy."
    )

st.divider()

# ==========================================
# WATER ANALYTICS
# ==========================================

st.subheader("🚰 Water Consumption Analytics")

initial_water = df["water_level"].max()

water_used = round(
    initial_water - water,
    2
)

st.metric(
    "Total Water Used",
    f"{water_used}%"
)

# ==========================================
# IRRIGATION HISTORY
# ==========================================

st.subheader("⚙ Irrigation Activity")

pump_on_count = len(
    df[df["pump_status"] == "ON"]
)

st.metric(
    "Pump Activations",
    pump_on_count
)

st.divider()

# ==========================================
# SOIL GAUGE
# ==========================================

st.subheader("🌱 Soil Moisture Gauge")

soil_fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=soil,
        title={"text": "Soil Moisture (%)"},
        gauge={
            "axis": {
                "range": [0, 100]
            }
        }
    )
)

st.plotly_chart(
    soil_fig,
    use_container_width=True
)

# ==========================================
# WATER GAUGE
# ==========================================

st.subheader("🚰 Water Tank Gauge")

water_fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=water,
        title={"text": "Water Tank Level (%)"},
        gauge={
            "axis": {
                "range": [0, 100]
            }
        }
    )
)

st.plotly_chart(
    water_fig,
    use_container_width=True
)

# ==========================================
# FARM HEALTH TREND
# ==========================================

st.subheader("💚 Farm Health Trend")

health_values = []

for _, row in df.iterrows():

    score = 100

    if row["soil_moisture"] < 35:
        score -= 30

    if row["water_level"] < 20:
        score -= 30

    if row["temperature"] > 40:
        score -= 20

    health_values.append(score)

trend_df = pd.DataFrame(
    {
        "Farm Health Score": health_values
    }
)

st.line_chart(trend_df)

# ==========================================
# HISTORICAL ANALYTICS
# ==========================================

st.subheader("📈 Historical Analytics")

st.line_chart(
    df[
        [
            "temperature",
            "humidity",
            "soil_moisture",
            "water_level"
        ]
    ]
)

# ==========================================
# DOWNLOAD REPORT
# ==========================================

st.subheader("📥 Download Sensor Report")

csv = df.to_csv(index=False)

st.download_button(
    label="Download CSV Report",
    data=csv,
    file_name="smart_agriculture_report.csv",
    mime="text/csv"
)

# ==========================================
# DATA TABLE
# ==========================================

st.subheader("📊 Sensor Data Records")

st.dataframe(
    df,
    use_container_width=True
)