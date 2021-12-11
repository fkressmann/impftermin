import uuid

from extensions.db import db


class Booking(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    ack_at = db.Column(db.DateTime)

    timeslot_id = db.Column(db.String(36), db.ForeignKey('timeslot.id'), nullable=False)
    timeslot = db.relationship('Timeslot', backref=db.backref('bookings'), lazy=False)

    def __repr__(self):
        return f"<Activity {self.name}>"
