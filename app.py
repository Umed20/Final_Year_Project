from flask import Flask, render_template, jsonify
from datetime import datetime
import json
import folium
import os
from models import db, SensorData
from sensors import (
    setup_gpio,
    get_fingerprint_status,
    get_vehicle_status,
    get_safety_metrics,
    get_location_data,
    send_sms_alert
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('postgresql://vehicle_blackbox_user:m95F2QWXkhoXCh7l6ddofhZXDtH1B8Nc@dpg-cvkjhu3uibrs73a21hc0-a.oregon-postgres.render.com/vehicle_blackbox', 'sqlite:///sensor_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Initialize GPIO
setup_gpio()

with app.app_context():
    db.create_all()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/sensor-data')
def get_sensor_data():
    security_status = {
        'fingerprint': get_fingerprint_status(),
        'intruder_detection': 'OFF',  # Add intruder sensor if needed
        'theft_detection': 'OFF'      # Add theft sensor if needed
    }
    
    vehicle_status = get_vehicle_status()
    safety_metrics = get_safety_metrics()
    location_data = get_location_data()
    
    # Check for alerts
    if (vehicle_status['accident_detection'] == 'ON' or 
        safety_metrics['alcohol_detection'] == 'ON' or 
        safety_metrics['gas_detection'] == 'ON'):
        alert_message = "ALERT: Abnormal conditions detected in vehicle!"
        send_sms_alert(alert_message, "YOUR_PHONE_NUMBER")  # Replace with actual phone number
    
    # Save to database
    sensor_data = SensorData(
        timestamp=datetime.now(),
        security_status=json.dumps(security_status),
        vehicle_status=json.dumps(vehicle_status),
        safety_metrics=json.dumps(safety_metrics),
        location_data=json.dumps(location_data)
    )
    db.session.add(sensor_data)
    db.session.commit()
    
    return jsonify({
        'security_status': security_status,
        'vehicle_status': vehicle_status,
        'safety_metrics': safety_metrics,
        'location_data': location_data
    })

if __name__ == '__main__':
    app.run(debug=True)