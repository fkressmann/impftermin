from sqlalchemy import func
from util import generate_uuid
from extensions.db import db
from util import generate_uuid



class Booking(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=True, unique=True)
    booked_at = db.Column(db.DateTime, default=func.now())
    ack_at = db.Column(db.DateTime)
    age = db.Column(db.String(10))
    vaccination = db.Column(db.String(100))

    timeslot_id = db.Column(db.String(36), db.ForeignKey('timeslot.id'), nullable=False)
    timeslot = db.relationship('Timeslot', backref=db.backref('bookings'), lazy=False)

    def __repr__(self):
        return f"<Activity {self.name}>"