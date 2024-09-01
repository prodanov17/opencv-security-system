from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Camera(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    armed = db.Column(db.Boolean, default=False)
    algorithm = db.Column(db.String(80), default='ml')
    source = db.Column(db.String(80), default='0')
    notifications_enabled = db.Column(db.Boolean, default=False)
    last_motion = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, armed=False, algorithm='ml', source='0', notifications_enabled=False):
        self.name = name
        self.armed = armed
        self.algorithm = algorithm
        self.source = source
        self.notifications_enabled = notifications_enabled

    def arm(self, algorithm):
        self.armed = True
        self.algorithm = algorithm
        db.session.add(self)  # Ensure the object is added to the session
        db.session.commit()

    def disarm(self):
        self.armed = False
        db.session.add(self)  # Ensure the object is added to the session
        db.session.commit()

    def motion_detected(self):
        self.last_motion = datetime.utcnow()
        db.session.add(self)  # Ensure the object is added to the session
        db.session.commit()

    def manage_notifications(self, enabled):
        self.notifications_enabled = enabled
        db.session.add(self)  # Ensure the object is added to the session
        db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'armed': self.armed,
            'algorithm': self.algorithm,
            'source': self.source,
            'last_motion': self.last_motion,
            'notifications_enabled': self.notifications_enabled

        }


class Detection(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    camera_id = db.Column(db.Integer, db.ForeignKey('camera.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, camera_id, url):
        self.camera_id = camera_id
        self.url = url

    def serialize(self):
        return {
            'id': self.id,
            'camera_id': self.camera_id,
            'url': self.url,
            'timestamp': self.timestamp,
            'camera': Camera.query.get(self.camera_id).serialize()
        }
