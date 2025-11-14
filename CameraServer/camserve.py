from flask import Flask, Response, request
import threading
import time

app = Flask(__name__)

# ---------------------------
# Global frame buffer in RAM
# ---------------------------
latest_frame = None
frame_lock = threading.Lock()

# ---------------------------
# ESP32-CAM POST endpoint
# ---------------------------
@app.route("/camera", methods=["POST"])
def receive_frame():
    global latest_frame

    frame_data = request.data
    if not frame_data:
        return "No frame received", 400

    # Thread-safe write
    with frame_lock:
        latest_frame = frame_data

    print("Frame received:", len(frame_data), "bytes")
    return "OK", 200


# ---------------------------
# Live MJPEG stream
# ---------------------------
@app.route("/live")
def live_feed():

    def generate():
        global latest_frame

        while True:
            with frame_lock:
                frame = latest_frame

            if frame is not None:
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                )

            time.sleep(0.05)  # ~20 FPS max

    return Response(
        generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# ---------------------------
# Run the Flask server
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
