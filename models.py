from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.String(10))
    alcohol_detection = db.Column(db.String(10))
    gas_detection = db.Column(db.String(10))
    light_level = db.Column(db.String(10))
    speed_level = db.Column(db.String(10))
    fingerprint_status = db.Column(db.String(10))
    accident_detection = db.Column(db.String(10))
    towed_status = db.Column(db.String(10))
    ignition_status = db.Column(db.String(10))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
