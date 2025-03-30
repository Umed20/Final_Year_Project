from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    security_status = db.Column(db.String(500), nullable=False)
    vehicle_status = db.Column(db.String(500), nullable=False)
    safety_metrics = db.Column(db.String(500), nullable=False)
    location_data = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<SensorData {self.timestamp}>'