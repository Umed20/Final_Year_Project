from flask import Flask, request, jsonify, render_template
from models import db, SensorData
from database import init_db

app = Flask(__name__)
init_db(app)

@app.route('/')
def dashboard():
    """Serve the dashboard page."""
    return render_template("dashboard.html")

@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    """Receive sensor data from Raspberry Pi."""
    data = request.json

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    new_entry = SensorData(
        temperature=data.get("temperature"),
        alcohol_detection=data.get("alcohol_detection"),
        gas_detection=data.get("gas_detection"),
        light_level=data.get("light_level"),
        speed_level=data.get("speed_level"),
        fingerprint_status=data.get("fingerprint_status"),
        accident_detection=data.get("accident_detection"),
        towed_status=data.get("towed_status"),
        ignition_status=data.get("ignition_status"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude")
    )
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({"message": "Sensor data received successfully"}), 201

@app.route('/api/sensor-data', methods=['GET'])
def get_sensor_data():
    """Fetch the latest sensor data and format it for the frontend."""
    latest_data = SensorData.query.order_by(SensorData.timestamp.desc()).first()

    if not latest_data:
        return jsonify({"error": "No sensor data available"}), 404

    response = {
        "security_status": {
            "fingerprint": latest_data.fingerprint_status,
            "intruder_detection": "Unknown",  # You can modify this based on actual data
            "theft_detection": "Unknown"
        },
        "vehicle_status": {
            "ignition": latest_data.ignition_status,
            "brake": "Unknown",  # Modify this if you have brake status data
            "towed_status": latest_data.towed_status,
            "accident_detection": latest_data.accident_detection
        },
        "safety_metrics": {
            "alcohol_detection": latest_data.alcohol_detection,
            "temperature": latest_data.temperature,
            "speed_level": latest_data.speed_level,
            "gas_detection": latest_data.gas_detection,
            "light_level": latest_data.light_level
        },
        "location_data": {
            "latitude": latest_data.latitude,
            "longitude": latest_data.longitude,
            "location_name": "Current Location"
        }
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
