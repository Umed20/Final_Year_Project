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
    data = request.json

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    new_entry = SensorData(
        temperature=data["safety_metrics"].get("temperature"),
        alcohol_detection=data["safety_metrics"].get("alcohol_detection"),
        gas_detection=data["safety_metrics"].get("gas_detection"),
        light_level=data["safety_metrics"].get("light_level"),
        speed_level=data["safety_metrics"].get("speed_level"),
        fingerprint_status=data.get("fingerprint_status"),
        accident_detection=data["vehicle_status"].get("accident_detection"),
        towed_status=data["vehicle_status"].get("towed_status"),
        ignition_status=data["vehicle_status"].get("ignition"),
        latitude=data["location_data"].get("latitude"),
        longitude=data["location_data"].get("longitude"),
    )

    db.session.add(new_entry)
    db.session.commit()

    return jsonify({"message": "Sensor data received successfully"}), 201

@app.route('/api/sensor-data', methods=['GET'])
def get_sensor_data():
    latest_data = SensorData.query.order_by(SensorData.timestamp.desc()).first()

    if not latest_data:
        return jsonify({"error": "No sensor data available"}), 404

    response = {
        "security_status": {
            "fingerprint": latest_data.fingerprint_status or "No Data",
            "intruder_detection": "N/A",
            "theft_detection": "N/A"
        },
        "vehicle_status": {
            "ignition": latest_data.ignition_status or "No Data",
            "brake": "N/A",
            "towed_status": latest_data.towed_status or "No Data",
            "accident_detection": latest_data.accident_detection or "No Data"
        },
        "safety_metrics": {
            "alcohol_detection": latest_data.alcohol_detection or "No Data",
            "temperature": latest_data.temperature or "No Data",
            "speed_level": latest_data.speed_level or "No Data",
            "gas_detection": latest_data.gas_detection or "No Data",
            "light_level": latest_data.light_level or "No Data"
        },
        "location_data": {
            "latitude": latest_data.latitude or 0,
            "longitude": latest_data.longitude or 0,
            "location_name": "Current Location"
        }
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
