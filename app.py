import os, time
from flask import Flask, request, jsonify

app = Flask(__name__)
telemetry_data = {}
latest_command = {}

@app.get("/")
def home():
    return "Drone HTTP Relay Server Running"

@app.post("/upload")
def upload():
    global telemetry_data
    telemetry_data = request.json or {}
    telemetry_data["timestamp"] = time.time()
    return jsonify({"status": "ok"})

@app.get("/telemetry")
def telemetry():
    if telemetry_data:
        return jsonify(telemetry_data)
    return jsonify({"error": "no_telemetry"})

@app.post("/command")
def send_command():
    global latest_command
    latest_command = request.json or {}
    latest_command["timestamp"] = time.time()
    return jsonify({"status": "queued"})

@app.get("/get_command")
def get_command():
    global latest_command
    if latest_command:
        cmd = dict(latest_command)
        latest_command.clear()
        return jsonify(cmd)
    return jsonify({"command": "none"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=5001)

