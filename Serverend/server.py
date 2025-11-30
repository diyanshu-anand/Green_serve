from flask import Flask, request, jsonify, send_file
import sqlite3
from datetime import datetime
import base64
from io import BytesIO

app = Flask(__name__)

# ------------------- GLOBAL -------------------
latest_frame = None  # store latest camera frame in memory

# ---------------------------------------------------
# Initialize database (run once)
# ---------------------------------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            pressure REAL,
            altitude REAL,
            soil_moisture REAL,
            uv_index REAL,
            pir_motion REAL,
            ir_detect REAL,
            gunfire INTEGER,
            CO_Quality REAL,
            AIR_Quality REAL,
            RAIN_Sensing REAL,
            gps_lat REAL,
            gps_lon REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------------------------------------------
# Home route
# ---------------------------------------------------
@app.route('/')
def home():
    return jsonify({"status":"API running successfully", "message":"Welcome to the Forest Monitoring World !!"}) 

# ---------------------------------------------------
# Upload route for sensors and/or camera
# ---------------------------------------------------
@app.route('/upload', methods=['POST'])
def upload_data():
    global latest_frame
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error":"No JSON data received"}), 400

        # Check if this is camera data
        if "camera_image" in data:
            # Decode base64 image
            img_data = base64.b64decode(data["camera_image"])
            latest_frame = BytesIO(img_data)  # store in memory
            print(f"[+] Camera frame received at {datetime.now()}")
            return jsonify({"status":"success", "message":"Camera frame stored"})

        # Otherwise assume sensor data
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO sensor_data (
                temperature, humidity, pressure, altitude,
                soil_moisture, uv_index, pir_motion, ir_detect,
                gunfire, CO_Quality, AIR_Quality, RAIN_Sensing,
                gps_lat, gps_lon, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("temperature"),
            data.get("humidity"),
            data.get("pressure"),
            data.get("altitude"),
            data.get("soil_moisture"),
            data.get("uv_index"),
            data.get("pir_motion"),
            data.get("ir_detect"),
            data.get("gunfire"),
            data.get("CO_Quality"),
            data.get("AIR_Quality"),
            data.get("RAIN_Sensing"),
            data.get("gps_lat"),
            data.get("gps_lon"),
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()

        print(f"[+] Sensor data received at {datetime.now()}")
        return jsonify({"status":"success", "message":"Sensor data stored successfully"})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------------
# Retrieve last 50 sensor readings
# ---------------------------------------------------
@app.route("/data", methods=["GET"])
def get_data():
    try:
        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 50") # Latest 50
        rows = cur.fetchall()
        conn.close()

        data = [dict(row) for row in rows]
        return jsonify({"status":"success", "data": data}), 200

    except Exception as e:
        return jsonify({"status":"error", "message": str(e)}), 500

# ---------------------------------------------------
# Live camera view route
# ---------------------------------------------------
@app.route("/live")
def live_camera():
    global latest_frame
    if latest_frame is None:
        return "No camera frame yet", 404
    latest_frame.seek(0)
    return send_file(latest_frame, mimetype='image/jpeg')

# ---------------------------------------------------
# Run server
# ---------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
