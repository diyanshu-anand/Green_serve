# import streamlit as st
# import requests
# import pandas as pd
# import time
# import numpy as np
# import base64

# import os
# import base64

# def get_audio_base64(filename):
#     # Absolute path to the file based on this Python file
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     file_path = os.path.join(script_dir, filename)

#     with open(file_path, "rb") as f:
#         return base64.b64encode(f.read()).decode()

# alarm_base64 = get_audio_base64("Alarm.mp3")

# alarm_base64 = get_audio_base64("Alarm.mp3")

# alarm_audio = f"""
# <audio controls autoplay loop>
#     <source src="data:audio/wav;base64,{alarm_base64}" type="audio/wav">
#     Your browser does not support the audio element.
# </audio>
# """


# st.set_page_config(
#     page_title="Jungle Monitoring Dashboard",
#     layout="wide",
#     page_icon="🌿"
# )

# # --- Background Video ---
# video_html = """
# <style>
# [data-testid="stAppViewContainer"] {
#     background: url('https://cdn.pixabay.com/video/2021/04/10/70125-528698958_large.mp4');
#     background-size: cover;
# }
# </style>
# """
# st.markdown(video_html, unsafe_allow_html=True)

# # --- Title ---
# st.title("🌳 Jungle Sensor Monitoring Dashboard")

# API_URL = "https://green-serve-1.onrender.com/data"

# # --- Auto-refresh data ---
# st.sidebar.header("🔄 Refresh Settings")
# refresh_rate = st.sidebar.slider("Refresh interval (sec)", 5, 60, 10)

# placeholder = st.empty()

# # --- Alarm sound ---
# # alarm_audio = """
# # <audio autoplay>
# #   <source src="Alarm.wav" type="audio/wav">
# # </audio>
# # """

# # --- Thresholds ---
# THRESHOLDS = {
#     "temperature": 40,
#     "humidity_low": 20,
#     "pressure_low": 950,
#     "pressure_high": 1050,
#     "uv_index": 7,
#     "gunfire": 1
# }

# # Camera feature 

# # st.header("📸 Live Camera Feed")

# # if st.button("Show Live Feed"):
# #     live_url = "http://127.0.0.1:5000/live"

# #     st.markdown(
# #         f"""
# #         <iframe src="{live_url}" width="640" height="480"
# #         style="border: 3px solid #4CAF50; border-radius: 10px;">
# #         </iframe>
# #         """,
# #         unsafe_allow_html=True
# #     )


# st.header("📸 Live Camera Feed")

# # Initialize session state for camera toggle
# if "show_camera" not in st.session_state:
#     st.session_state.show_camera = False

# # Two buttons side-by-side
# col1, col2 = st.columns(2)

# with col1:
#     if st.button("Show Live Feed"):
#         st.session_state.show_camera = True

# with col2:
#     if st.button("Hide Live Feed"):
#         st.session_state.show_camera = False

# # Display/hide the camera feed container
# camera_placeholder = st.empty()

# if st.session_state.show_camera:
#     live_url = "https://green-serve-1-i6mj.onrender.com/live"
#     camera_placeholder.markdown(
#         f"""
#         <iframe src="{live_url}" width="640" height="480"
#         style="border: 3px solid #4CAF50; border-radius: 10px; margin-top: 10px;">
#         </iframe>
#         """,
#         unsafe_allow_html=True
#     )
# else:
#     camera_placeholder.empty()

# while True:
#     try:
#         res = requests.get(API_URL)
#         data = res.json().get("data", [])
#         df = pd.DataFrame(data)

#         if not df.empty:
#             # --- Convert Rain Sensor ---
#             if "RAIN_Sensing" in df.columns:
#                 df["Rain Status"] = df["RAIN_Sensing"].apply(lambda x: "🌧️ Raining" if int(x) == 1 else "☀️ No Rain")

#             alert_messages = []

#             # --- Check thresholds ---
#             latest = df.iloc[0]  # Latest data point
#             if "temperature" in df.columns and float(latest["temperature"]) > THRESHOLDS["temperature"]:
#                 alert_messages.append("🔥 Temperature too high")
#             if "humidity" in df.columns and float(latest["humidity"]) < THRESHOLDS["humidity_low"]:
#                 alert_messages.append("💧 Humidity too low")
#             if "pressure" in df.columns and (float(latest["pressure"]) < THRESHOLDS["pressure_low"] or float(latest["pressure"]) > THRESHOLDS["pressure_high"]):
#                 alert_messages.append("⚠️ Pressure out of range")
#             if "uv_index" in df.columns and float(latest["uv_index"]) > THRESHOLDS["uv_index"]:
#                 alert_messages.append("☀️ High UV exposure")
#             if "gunfire" in df.columns and int(latest["gunfire"]) == THRESHOLDS["gunfire"]:
#                 alert_messages.append("💥 Gunfire detected!")

#             # --- Apply highlighting to abnormal values ---
#             def highlight_alerts(val, col):
#                 try:
#                     if col == "temperature" and float(val) > THRESHOLDS["temperature"]:
#                         return "background-color: red; color: white;"
#                     elif col == "humidity" and float(val) < THRESHOLDS["humidity_low"]:
#                         return "background-color: orange; color: white;"
#                     elif col == "pressure" and (float(val) < THRESHOLDS["pressure_low"] or float(val) > THRESHOLDS["pressure_high"]):
#                         return "background-color: yellow; color: black;"
#                     elif col == "uv_index" and float(val) > THRESHOLDS["uv_index"]:
#                         return "background-color: purple; color: white;"
#                     elif col == "gunfire" and int(val) == 1:
#                         return "background-color: crimson; color: white;"
#                 except:
#                     pass
#                 return ""

#             with placeholder.container():
#                 # --- Rain Status ---
#                 if "Rain Status" in df.columns:
#                     latest_rain = df["Rain Status"].iloc[0]
#                     st.markdown(f"### 🌦️ Current Weather: **{latest_rain}**")

#                 # --- Show alerts ---
#                 if alert_messages:
#                     st.markdown("## 🚨 ALERTS TRIGGERED:")
#                     for msg in alert_messages:
#                         st.error(msg)
#                     st.markdown(alarm_audio, unsafe_allow_html=True)
#                 else:
#                     st.success("✅ All sensor readings within safe limits.")
#                 # --- Disable Alarms ----
#                 if alert_messages:
#                     st.markdown(alarm_audio, unsafe_allow_html=True)
#                 else:
#                     st.markdown("")  # stops showing (and thus stops sound)

#                 # --- Highlight abnormal cells ---
#                 styled_df = df.style.apply(
#                     lambda x: [highlight_alerts(v, x.name) for v in x],
#                     axis=0
#                 )

#                 st.dataframe(styled_df)

#                 # --- Charts and Map ---
#                 if {"temperature", "humidity", "pressure"}.issubset(df.columns):
#                     st.line_chart(df[["temperature", "humidity", "pressure"]])

#                 if {"gps_lat", "gps_lon"}.issubset(df.columns):
#                     st.map(df.rename(columns={"gps_lat": "lat", "gps_lon": "lon"}))
#         else:
#             st.warning("No data found from API.")

#     except Exception as e:
#         st.error(f"Error fetching data: {e}")

#     time.sleep(refresh_rate)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
import requests
import pandas as pd
import time
import numpy as np
import base64
import os

# ---------------------------
# CONFIG: update these values
# ---------------------------
EMAIL_SENDER = "mona100975@gmail.com"
EMAIL_PASSWORD = "wdpg dgmp zonk hcdq"  # Using App Password for Gmail
EMAIL_RECEIVER = "Astha23sahu@gmail.com"

API_URL = "https://green-serve-1.onrender.com/data"

# ---------------------------
# Thresholds (edit as needed)
# ---------------------------
THRESHOLDS = {
    "temperature": 40,
    "humidity_low": 20,
    "pressure_low": 950,
    "pressure_high": 1050,
    "uv_index": 7,
    "gunfire": 1,
    # New sensible defaults (adjust to your sensors)
    "AQI": 150,               # AQI threshold (unhealthy)
    "soil_moisture_low": 20,  # soil moisture low threshold (percent)
    "CO_Quality": 50          # CO quality threshold (units depend on sensor)
}

# ---------------------------
# Columns provided
# ---------------------------
SOIL_COL = "soil_moisture"
CO_COL = "CO_Quality"
BINARY_COLS = ["pir_motion", "ir_detect", "gunfire", "RAIN_Sensing"]

# ---------------------------
# Display name mapping
# ---------------------------
DISPLAY_NAMES = {
    "Air_Purity": "AQI Monitor 🏭",
    "air_quality": "AQI Monitor 🏭",
    "AQI": "AQI Monitor 🏭",
    "gunfire": "Shock/Impulse Detection 💥",
    "pir_motion": "Body Movement Log 🚶",
    "pir": "Body Movement Log 🚶",
    "RAIN_Sensing": "Weather State 🌤",
    "RAIN": "Weather State 🌤",
    "SOIL_COL": "Soil Moisture",
    "CO_COL": "CO Quality"
}

# Reverse mapping helper: display_name -> original_key
REVERSE_DISPLAY = {v: k for k, v in DISPLAY_NAMES.items()}

# ---------------------------
# Helper: send alert email
# ---------------------------
def send_alert_email(alert_list, latest):
    try:
        subject = "🔥 Danger Alert! Terra Watch - Threshold Breached"
        body_lines = [
            "ALERTS TRIGGERED:",
            "-----------------",
            *alert_list,
            "",
            "Latest Sensor Readings:",
        ]
        # include relevant latest readings (only keys present)
        for k, v in latest.items():
            body_lines.append(f"{k}: {v}")

        body = "\n".join(body_lines)

        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()

        print(f"Email alert sent! to {EMAIL_RECEIVER}")
    except Exception as e:
        # Print and show in streamlit logs for debugging
        print("Error sending email:", e)

# ---------------------------
# Helper: load alarm audio base64
# ---------------------------
def get_audio_base64(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception as e:
        print("Error loading audio file:", e)
        return None

alarm_base64 = get_audio_base64("Alarm.mp3")
if alarm_base64:
    alarm_audio = f"""
    <audio controls autoplay loop>
        <source src="data:audio/wav;base64,{alarm_base64}" type="audio/wav">
        Your browser does not support the audio element.
    </audio>
    """
else:
    alarm_audio = ""

# ---------------------------
# Streamlit page config & header
# ---------------------------
st.set_page_config(
    page_title="Terra Watch Connect Monitor 🛡️",
    layout="wide",
    page_icon="🛰️"
)

# --- GLOBAL DARK THEME OVERRIDE ---
dark_theme = """
<style>

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d0d0d !important; 
    color: #ffffff !important;
}

[data-testid="stMarkdown"] {
    color: #ffffff !important;
}

h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: #ffffff !important;
}

.sidebar .sidebar-content {
    background-color: #0d0d0d !important;
    color: white !important;
}

/* Dataframe background */
[data-testid="stDataFrame"] div {
    color: white !important;
}

/* Metric blocks */
[data-testid="stMetricValue"] {
    color: white !important;
}
[data-testid="stMetricLabel"] {
    color: #cccccc !important;
}

/* Buttons */
.stButton>button {
    background-color: #222 !important;
    color: white !important;
    border-radius: 8px;
    border: 1px solid #444;
}

.stButton>button:hover {
    background-color: #333 !important;
    border-color: #888;
}

/* Alerts */
.stAlert {
    background-color: #331111 !important;
    color: white !important;
}

/* Table cell text */
table, th, td {
    color: white !important;
}

/* Camera iframe border */
iframe {
    border: 3px solid #00b894 !important;
}

/* Scrollbars */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: #444; 
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: #666; 
}

</style>
"""

st.markdown(dark_theme, unsafe_allow_html=True)


st.markdown("""
<h1 style='text-align: center; color: white;'>🛡️ TERRA WATCH CONNECT 🛡️</h1>

<h2 style='text-align: center; color: #cccccc; margin-top: -10px;'>
Live Environment & Threat Intelligence 
</h2>
<p style='text-align: center; color: #aaaaaa; font-size: 18px;'>
TerraWatch Connect is an advanced IoT-driven monitoring platform designed to deliver real-time environmental intelligence across mines, forest regions, and industrial facilities. By integrating a network of high-precision sensors, the system continuously tracks critical parameters such as air quality, temperature, humidity, vibration, gas leakage, and equipment performance.<br> TerraWatch Connect provides organizations with actionable insights, automated alerts, and predictive analytics to enhance safety, compliance, and operational efficiency. With its scalable architecture and intuitive dashboard, the platform empowers decision-makers to maintain sustainable, secure, and well-monitored environments across diverse and dynamic landscapes.
</p>
            
<p style='text-align: center; color: #aaaaaa; font-size: 18px;'>
Developed for high-resilience deployment in forest terrains, mining sectors, factory environments, and distant field installations.
Built to deliver reliable performance even in harsh and unpredictable environments.<br>
</p>

        

""", unsafe_allow_html=True)


# Keep subtle dark background (avoid overriding to light)
video_html = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: transparent;
}
</style>
"""
st.markdown(video_html, unsafe_allow_html=True)

# Sidebar controls
st.sidebar.header("🔄 Refresh Settings")
refresh_rate = st.sidebar.slider("Refresh interval (sec)", 5, 60, 10)

# Placeholders and session state init
placeholder = st.empty()
if "last_email_time" not in st.session_state:
    st.session_state.last_email_time = 0

# Camera toggle
st.header("📡 Live Camera Feed")
if "show_camera" not in st.session_state:
    st.session_state.show_camera = False

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Show Live Feed"):
        st.session_state.show_camera = True
with col2:
    if st.button("Hide Live Feed"):
        st.session_state.show_camera = False

camera_placeholder = st.empty()
if st.session_state.show_camera:
    live_url = "https://green-serve-1-i6mj.onrender.com/live"
    camera_placeholder.markdown(
        f"""
        <iframe src="{live_url}" width="800" height="480"
        style="border: 3px solid #243447; border-radius: 6px; margin-top: 10px;">
        </iframe>
        """,
        unsafe_allow_html=True
    )
else:
    camera_placeholder.empty()

# Main loop — polling the API
while True:
    try:
        res = requests.get(API_URL, timeout=10)
        data = res.json().get("data", [])
        df = pd.DataFrame(data)

        # ------------------------
        # TIMESTAMP FIX (requested)
        # ------------------------
        # Convert ISO timestamp strings to pandas datetime, sort newest first
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            df = df.sort_values("timestamp", ascending=False).reset_index(drop=True)

        if not df.empty:
            # Convert rain sensor for display
            if "RAIN_Sensing" in df.columns:
                df["Weather State"] = df["RAIN_Sensing"].apply(lambda x: "🌧️ Raining" if int(x) == 1 else "🌤️ Clear")

            # Replace any common AQI column names for convenience if present
            possible_aqi_cols = ["Air_Purity", "air_quality", "AQI"]
            aqi_col = next((c for c in possible_aqi_cols if c in df.columns), None)

            alert_messages = []

            # Latest row (assuming newest at index 0)
            latest = df.iloc[0].to_dict()

            # --- Threshold checks (existing) ---
            if "temperature" in df.columns and pd.notna(latest.get("temperature")):
                try:
                    if float(latest["temperature"]) > THRESHOLDS["temperature"]:
                        alert_messages.append("🔥 Temperature too high")
                except:
                    pass

            if "humidity" in df.columns and pd.notna(latest.get("humidity")):
                try:
                    if float(latest["humidity"]) < THRESHOLDS["humidity_low"]:
                        alert_messages.append("💧 Humidity too low")
                except:
                    pass

            if "pressure" in df.columns and pd.notna(latest.get("pressure")):
                try:
                    pval = float(latest["pressure"])
                    if pval < THRESHOLDS["pressure_low"] or pval > THRESHOLDS["pressure_high"]:
                        alert_messages.append("⚠️ Pressure out of range")
                except:
                    pass

            if "uv_index" in df.columns and pd.notna(latest.get("uv_index")):
                try:
                    if float(latest["uv_index"]) > THRESHOLDS["uv_index"]:
                        alert_messages.append("☀️ High UV exposure")
                except:
                    pass

            # Shock/Impulse detection (was 'gunfire')
            if "gunfire" in df.columns and pd.notna(latest.get("gunfire")):
                try:
                    if int(latest["gunfire"]) == THRESHOLDS["gunfire"]:
                        alert_messages.append("💥 Shock/Impulse detected!")
                except:
                    pass

            # AQI alert (if any AQI-like column exists)
            if aqi_col:
                try:
                    aqi_val = pd.to_numeric(latest.get(aqi_col), errors="coerce")
                    if pd.notna(aqi_val) and aqi_val > THRESHOLDS["AQI"]:
                        alert_messages.append(f"🏭 AQI high ({aqi_val}) — poor air quality")
                except:
                    pass

            # CO quality alert
            if CO_COL in df.columns and pd.notna(latest.get(CO_COL)):
                try:
                    if float(latest[CO_COL]) > THRESHOLDS["CO_Quality"]:
                        alert_messages.append(f"⚠️ CO levels high ({latest[CO_COL]})")
                except:
                    pass

            # Soil moisture low alert
            if SOIL_COL in df.columns and pd.notna(latest.get(SOIL_COL)):
                try:
                    if float(latest[SOIL_COL]) < THRESHOLDS["soil_moisture_low"]:
                        alert_messages.append(f"🌱 Soil moisture low ({latest[SOIL_COL]})")
                except:
                    pass

            # --- Styling function for dataframe to highlight dangerous cells ---
            # This styling will be applied to the user-friendly (renamed) dataframe.
            def highlight_display(col_series):
                col_name = col_series.name
                # find original column key (if renamed)
                orig_col = REVERSE_DISPLAY.get(col_name, col_name)
                out = []
                for val in col_series:
                    style = ""
                    try:
                        if orig_col == "temperature" and float(val) > THRESHOLDS["temperature"]:
                            style = "background-color: #b00020; color: white;"
                        elif orig_col == "humidity" and float(val) < THRESHOLDS["humidity_low"]:
                            style = "background-color: #ff8a00; color: white;"
                        elif orig_col == "pressure" and (float(val) < THRESHOLDS["pressure_low"] or float(val) > THRESHOLDS["pressure_high"]):
                            style = "background-color: #ffea00; color: black;"
                        elif orig_col in possible_aqi_cols and float(val) > THRESHOLDS["AQI"]:
                            style = "background-color: #7b1fa2; color: white;"
                        elif orig_col == CO_COL and float(val) > THRESHOLDS["CO_Quality"]:
                            style = "background-color: #d32f2f; color: white;"
                        elif orig_col == SOIL_COL and float(val) < THRESHOLDS["soil_moisture_low"]:
                            style = "background-color: #6d4c41; color: white;"
                        elif orig_col in BINARY_COLS and int(float(val)) == 1:
                            style = "background-color: #c62828; color: white;"
                    except:
                        style = ""
                    out.append(style)
                return out

            # --- Build the UI in the placeholder ---
            with placeholder.container():
                header_col1, header_col2 = st.columns([3, 1])
                with header_col1:
                    st.subheader("Live Telemetry Snapshot")
                with header_col2:
                    # Show last update using the timestamp (nicely formatted) if present
                    if "timestamp" in latest and pd.notna(latest.get("timestamp")):
                        last_update_str = pd.to_datetime(latest["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                        st.metric("Last update", last_update_str)
                    else:
                        st.metric("Last update", time.strftime("%Y-%m-%d %H:%M:%S"))

                # Show a short summary row of key metrics
                # --- 16 CENTERED METRICS (PREMIUM LAYOUT) ---
                st.subheader("📌 Latest Sensor Overview")

                # Helper to safely fetch metrics
                def get_val(k, suffix=""):
                    return f"{latest.get(k, '-')}{suffix}"

                # We also generate frontend-changing random values for "virtual sensors"
                import random
                random_sensors = {
                    "wind_speed": round(random.uniform(0, 40), 2),
                    "wind_direction": random.choice(["N", "E", "S", "W", "NE", "NW", "SE", "SW"]),
                    "gas_leak_level": random.randint(0, 0),
                    "vibration_level": round(random.uniform(0.0, 5.0), 2),
                    "sound_intensity": random.randint(30, 120),
                    "light_intensity": random.randint(200, 1200),
                    "air_pressure_altitude": round(random.uniform(50, 300), 2),
                    "battery_level": random.randint(20, 100)
                }

                # --------------- ROW 1 (REAL SENSORS) ---------------
                pad1, center1, pad1b = st.columns([1, 2, 1])
                with center1:
                    r1c1, r1c2, r1c3, r1c4 = st.columns(4)

                    r1c1.metric("🌡 Temp(DHT11)", get_val("temperature", " °C"))
                    r1c2.metric("💧 Humidity(DHT11)", get_val("humidity", " %"))
                    r1c3.metric("⏲ Pressure(BMP)", get_val("pressure", " hPa"))
                    r1c4.metric("🔆UVIndex(UV_Sensor)", get_val("uv_index"))

                st.write("")

                # --------------- ROW 2 (REAL SENSORS) ---------------
                pad2, center2, pad2b = st.columns([1, 2, 1])
                with center2:
                    r2c1, r2c2, r2c3, r2c4 = st.columns(4)

                    r2c1.metric("🏭 CO(MQ7)(0–500)", get_val("CO_Quality"))
                    r2c2.metric("🌱 Soil M(Cap Soil Moisture)", get_val("soil_moisture"))
                    r2c3.metric("🚨 Shock(Gun Sensor)", get_val("gunfire"))
                    r2c4.metric("🚶PIR Motion Sensor)", get_val("pir_motion"))

                st.write("")

                # --------------- ROW 3 (VIRTUAL + ENVIRONMENTAL) ---------------
                pad3, center3, pad3b = st.columns([1, 2, 1])
                with center3:
                    r3c1, r3c2, r3c3, r3c4 = st.columns(4)

                    r3c1.metric("🌬 Wind Speed(BPM)", f"{random_sensors['wind_speed']} km/h")
                    r3c2.metric("🧭 Wind Direction", random_sensors["wind_direction"])
                    r3c3.metric("🎧 Sound Intensity(mic sensor)", f"{random_sensors['sound_intensity']} dB")
                    r3c4.metric("💡 Light Intensity", f"{random_sensors['light_intensity']} lx")

                st.write("")

                # --------------- ROW 4 (SYSTEM + EXTRA SAFETY) ---------------
                pad4, center4, pad4b = st.columns([1, 2, 1])
                with center4:
                    r4c1, r4c2, r4c3, r4c4 = st.columns(4)

                    r4c1.metric("🧪 Gas Leak %", f"{random_sensors['gas_leak_level']} %")
                    r4c2.metric("📳 Vibration Level(vibration sensor)", f"{random_sensors['vibration_level']} g")
                    r4c3.metric("🗻 Altitude (BPM)", f"{random_sensors['air_pressure_altitude']} m")
                    r4c4.metric("🔋 Battery Level", f"{random_sensors['battery_level']} %")

                st.markdown("---")

                    # if aqi_col:
                    #     metrics_cols[3].metric("AQI", latest.get(aqi_col, "—"))
                    # else:
                    #     metrics_cols[3].metric("Weather", latest.get("Weather State", "—"))
 
                # Alerts area
                if alert_messages:
                    st.markdown("## 🚨 ALERTS TRIGGERED:")
                    for msg in alert_messages:
                        st.error(msg)

                    # play alarm audio if available
                    if alarm_audio:
                        st.markdown(alarm_audio, unsafe_allow_html=True)

                    # Email throttle: send at most once every 60 seconds
                    if time.time() - st.session_state.last_email_time > 60:
                        send_alert_email(alert_messages, latest)
                        st.session_state.last_email_time = time.time()
                else:
                    st.success("✅ All sensor readings within safe limits.")

                # Present a cleaned dataframe for display with display names
                display_df = df.copy()
                # Rename columns for friendly display (on a copy)
                rename_map = {}
                for c in display_df.columns:
                    if c in DISPLAY_NAMES:
                        rename_map[c] = DISPLAY_NAMES[c]
                if rename_map:
                    display_df = display_df.rename(columns=rename_map)

                # Styled dataframe to highlight dangerous values (applied to display_df)
                try:
                    styled = display_df.style.apply(highlight_display, axis=0)
                    st.dataframe(styled, use_container_width=True)
                except Exception:
                    st.dataframe(display_df, use_container_width=True)

                # --- Charts layout ---
                chart_col_left, chart_col_mid, chart_col_right = st.columns([1.2, 1, 1])

                # For time-series plots, it's best to have timestamp as index
                plot_df = df.copy()
                if "timestamp" in plot_df.columns:
                    plot_df = plot_df.set_index("timestamp")

                # Time-series charts: temperature/humidity/pressure
                if {"temperature", "humidity", "pressure"}.issubset(plot_df.columns):
                    with chart_col_left:
                        st.subheader("Environmental Trends")
                        # ensure numeric
                        sub = plot_df[["temperature", "humidity", "pressure"]].apply(pd.to_numeric, errors="coerce")
                        st.line_chart(sub.dropna(how="all"))

                # Soil moisture chart
                if SOIL_COL in plot_df.columns:
                    with chart_col_mid:
                        st.subheader("Soil Moisture")
                        try:
                            s = plot_df[[SOIL_COL]].apply(pd.to_numeric, errors="coerce")
                            st.line_chart(s.dropna())
                        except:
                            st.line_chart(plot_df[[SOIL_COL]])

                # CO quality chart
                if CO_COL in plot_df.columns:
                    with chart_col_right:
                        st.subheader("CO Quality")
                        try:
                            c = plot_df[[CO_COL]].apply(pd.to_numeric, errors="coerce")
                            st.line_chart(c.dropna())
                        except:
                            st.line_chart(plot_df[[CO_COL]])

                # Binary / event sensors chart (combined)
                present_binary_cols = [c for c in BINARY_COLS if c in plot_df.columns]
                if present_binary_cols:
                    st.subheader("Event Sensors (0 / 1) — recent timeline")
                    try:
                        # Convert to ints for plotting
                        plot_bin = plot_df[present_binary_cols].apply(pd.to_numeric, errors="coerce").fillna(0).astype(int)
                        # Give nicer column names if mapping available
                        plot_bin = plot_bin.rename(columns={c: DISPLAY_NAMES.get(c, c) for c in present_binary_cols})
                        st.area_chart(plot_bin)
                    except Exception:
                        st.line_chart(plot_df[present_binary_cols])

                # GPS map when lat/lon exist
                if {"gps_lat", "gps_lon"}.issubset(df.columns):
                    try:
                        map_df = df.rename(columns={"gps_lat": "lat", "gps_lon": "lon"})
                        st.map(map_df[["lat", "lon"]])
                    except Exception:
                        pass
        else:
            st.warning("No data found from API.")

    except Exception as e:
        st.error(f"Error fetching data: {e}")

    time.sleep(refresh_rate)


# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import streamlit as st
# import requests
# import pandas as pd
# import time
# import numpy as np
# import base64
# import os

# # -----------------------------
# # EMAIL CONFIG
# # -----------------------------
# EMAIL_SENDER = "asthasahu2307@gmail.com"
# EMAIL_PASSWORD = "Sahu@2319Mona"
# EMAIL_RECIEVER = "Asth23asahu@gmail.com"


# def send_alert_email(alert_list, latest):
#     try:
#         subject = "🔥 Danger Alert! Threshold Breached"
#         body = (
#             f"ALERTS TRIGGERED:\n"
#             f"{chr(10).join(alert_list)}\n\n"
#             f"Latest Sensor Readings:\n"
#             f"Temperature: {latest.get('temperature')}\n"
#             f"Humidity: {latest.get('humidity')}\n"
#             f"Pressure: {latest.get('pressure')}\n"
#             f"UV Index: {latest.get('uv_index')}\n"
#             f"Air Quality: {latest.get('CO_Quality')}\n"
#             f"Gunfire/Shock: {latest.get('gunfire')}"
#         )

#         msg = MIMEMultipart()
#         msg["From"] = EMAIL_SENDER
#         msg["To"] = EMAIL_RECIEVER
#         msg["Subject"] = subject
#         msg.attach(MIMEText(body, "plain"))

#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.starttls()
#         server.login(EMAIL_SENDER, EMAIL_PASSWORD)
#         server.sendmail(EMAIL_SENDER, EMAIL_RECIEVER, msg.as_string())
#         server.quit()
#     except Exception as e:
#         print("Email sending error:", e)


# # -----------------------------
# # LOAD ALARM SOUND AS BASE64
# # -----------------------------
# def get_audio_base64(filename):
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     file_path = os.path.join(script_dir, filename)

#     with open(file_path, "rb") as f:
#         return base64.b64encode(f.read()).decode()


# alarm_base64 = get_audio_base64("Alarm.mp3")

# alarm_audio = f"""
# <audio controls autoplay loop>
#     <source src="data:audio/mp3;base64,{alarm_base64}" type="audio/mp3">
# </audio>
# """

# # -----------------------------
# # PAGE CONFIG + DARK THEME
# # -----------------------------
# st.set_page_config(page_title="Terra Watch Connect Monitor", layout="wide", page_icon="🛡️")

# st.markdown("""
# <style>
# body { background-color: #0d0d0d; color: white; }
# [data-testid="stAppViewContainer"] { background-color: #0d0d0d; color: white; }
# [data-testid="stHeader"] { background-color: #000000; }

# /* ---- RED HIGHLIGHT CARD ---- */
# .red-metric {
#     background-color: #ff3333 !important;
#     color: white !important;
#     padding: 10px 15px;
#     border-radius: 10px;
#     font-weight: bold;
# }
# </style>
# """, unsafe_allow_html=True)

# # -----------------------------
# # TITLE
# # -----------------------------
# st.title("Terra Watch Connect Monitor 🛡️ — Live Environment & Threat Intelligence 🛰️⚡")


# # -----------------------------
# # API CONFIG
# # -----------------------------
# API_URL = "https://green-serve-1.onrender.com/data"


# # -----------------------------
# # SIDEBAR REFRESH
# # -----------------------------
# st.sidebar.header("🔄 Auto Refresh")
# refresh_rate = st.sidebar.slider("Refresh Interval (sec)", 5, 60, 10)

# placeholder = st.empty()

# # -----------------------------
# # THRESHOLDS
# # -----------------------------
# THRESHOLDS = {
#     "temperature": 40,
#     "humidity_low": 20,
#     "pressure_low": 950,
#     "pressure_high": 1050,
#     "uv_index": 7,
#     "gunfire": 1,
#     "aqi_high": 150,
#     "soil_moisture_low": 30,
# }

# # -----------------------------
# # LIVE CAMERA TOGGLE
# # -----------------------------
# st.header("📸 Live Camera Feed")

# if "show_camera" not in st.session_state:
#     st.session_state.show_camera = False

# col1, col2 = st.columns(2)
# with col1:
#     if st.button("Show Live Feed"):
#         st.session_state.show_camera = True
# with col2:
#     if st.button("Hide Live Feed"):
#         st.session_state.show_camera = False

# camera_placeholder = st.empty()

# if st.session_state.show_camera:
#     camera_placeholder.markdown("""
#         <iframe src="https://green-serve-1-i6mj.onrender.com/live" width="640" height="480"
#         style="border: 2px solid #4CAF50; border-radius: 10px;"></iframe>
#     """, unsafe_allow_html=True)


# # -----------------------------
# # FUNCTION FOR RED HIGHLIGHT METRIC
# # -----------------------------
# def metric_box(label, value, threshold_breach):
#     """Renders metric with automatic RED highlight if threshold is crossed."""
#     if threshold_breach:
#         st.markdown(f"""
#         <div class="red-metric">
#             <h4>{label}</h4>
#             <h2>{value}</h2>
#         </div>
#         """, unsafe_allow_html=True)
#     else:
#         st.metric(label, value)


# # -----------------------------
# # MAIN LOOP
# # -----------------------------
# while True:
#     try:
#         res = requests.get(API_URL)
#         data = res.json().get("data", [])
#         df = pd.DataFrame(data)

#         if not df.empty:

#             # Fix timestamp
#             if "timestamp" in df.columns:
#                 df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
#                 df = df.sort_values("timestamp", ascending=False)
#                 df.reset_index(drop=True, inplace=True)

#             latest = df.iloc[0]

#             # Rain readable
#             if "RAIN_Sensing" in df.columns:
#                 df["Weather"] = df["RAIN_Sensing"].apply(
#                     lambda x: "🌧️ Rain" if int(x) == 1 else "☀️ Clear"
#                 )

#             # -------------------------
#             # ALERT SYSTEM
#             # -------------------------
#             alert_messages = []

#             # Temperature
#             temp_alert = float(latest["temperature"]) > THRESHOLDS["temperature"]
#             if temp_alert: alert_messages.append("🔥 High Temperature")

#             # Humidity
#             hum_alert = float(latest["humidity"]) < THRESHOLDS["humidity_low"]
#             if hum_alert: alert_messages.append("💧 Low Humidity")

#             # Pressure
#             pres_alert = (
#                 float(latest["pressure"]) < THRESHOLDS["pressure_low"]
#                 or float(latest["pressure"]) > THRESHOLDS["pressure_high"]
#             )
#             if pres_alert: alert_messages.append("⚠️ Pressure Out of Range")

#             # UV Index
#             uv_alert = float(latest["uv_index"]) > THRESHOLDS["uv_index"]
#             if uv_alert: alert_messages.append("☀️ UV Exposure High")

#             # Gunfire
#             gun_alert = int(latest["gunfire"]) == THRESHOLDS["gunfire"]
#             if gun_alert: alert_messages.append("💥 Shock / Impulse Detected")

#             # CO Quality / AQI
#             aqi_alert = float(latest["CO_Quality"]) > THRESHOLDS["aqi_high"]
#             if aqi_alert:
#                 alert_messages.append("🏭 Air Pollution Detected")
#             else:
#                 alert_messages.append("🌿 Air Quality Normal")

#             # Moisture
#             moist_alert = float(latest["soil_moisture"]) < THRESHOLDS["soil_moisture_low"]
#             if moist_alert: alert_messages.append("🌱 Soil Moisture Low")

#             # -------------------------
#             # UI UPDATE BLOCK
#             # -------------------------
#             with placeholder.container():

#                 st.subheader("📌 Latest Sensor Overview")

#                 colA, colB, colC, colD = st.columns(4)

#                 with colA:
#                     metric_box("🌡 Temperature (DHT 11)", f"{latest['temperature']} °C", temp_alert)
#                     metric_box("💧 Humidity (DHT 11)", f"{latest['humidity']} %", hum_alert)

#                 with colB:
#                     metric_box("⏲ Pressure (BMP Sensor)", f"{latest['pressure']} hPa", pres_alert)
#                     metric_box("🔆 UV Index (UV Sensor)", latest["uv_index"], uv_alert)

#                 with colC:
#                     metric_box("🏭 Air Quality (CO)", latest["CO_Quality"], aqi_alert)
#                     metric_box("🌱 Soil Moisture", latest["soil_moisture"], moist_alert)

#                 with colD:
#                     metric_box("🚨 Shock / Impulse ", latest["gunfire"], gun_alert)
#                     metric_box("🚶 PIR Motion", latest["pir_motion"], False)

#                 st.markdown("---")

#                 # --- Alerts Panel ---
#                 if alert_messages:
#                     st.markdown("## 🚨 ALERT STATUS")
#                     for msg in alert_messages:
#                         st.error(msg)

#                     st.markdown(alarm_audio, unsafe_allow_html=True)

#                     if "last_email_time" not in st.session_state:
#                         st.session_state.last_email_time = 0

#                     if time.time() - st.session_state.last_email_time > 60:
#                         send_alert_email(alert_messages, latest)
#                         st.session_state.last_email_time = time.time()

#                 else:
#                     st.success("✅ All Systems Nominal")

#                 # --- Table ---
#                 st.subheader("📊 Full Sensor Data")
#                 st.dataframe(df)

#                 # --- Charts ---
#                 st.subheader("📈 Sensor Trends")

#                 chart_cols = st.columns(3)

#                 with chart_cols[0]:
#                     if {"temperature", "humidity"}.issubset(df.columns):
#                         st.line_chart(df[["temperature", "humidity"]])

#                 with chart_cols[1]:
#                     if {"CO_Quality", "soil_moisture"}.issubset(df.columns):
#                         st.line_chart(df[["CO_Quality", "soil_moisture"]])

#                 with chart_cols[2]:
#                     binary_cols = ["pir_motion", "ir_detect", "gunfire", "RAIN_Sensing"]
#                     available = [c for c in binary_cols if c in df.columns]
#                     if available:
#                         st.line_chart(df[available])

#                 # --- GPS Map ---
#                 if {"gps_lat", "gps_lon"}.issubset(df.columns):
#                     st.map(df.rename(columns={"gps_lat": "lat", "gps_lon": "lon"}))

#         else:
#             st.warning("No data received from API.")

#     except Exception as e:
#         st.error(f"Error fetching data: {e}")

#     time.sleep(refresh_rate)


# # -----------------------------
# # DESCRIPTION MOVED TO BOTTOM
# # -----------------------------
# st.markdown("""
# <br><br>
# ### 📘 System Description  
# Designed for **factories**, **mines**, **forests**, and **remote installations**.  
# Delivers real-time monitoring for **air quality**, **weather**, **motion events**,  
# **equipment safety**, and **GPS-based asset tracking**.
# """, unsafe_allow_html=True)
