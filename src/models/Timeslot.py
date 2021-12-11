from util import generate_uuid
from extensions.db import db


class Timeslot(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    start_time = db.Column(db.DateTime)
    capacity = db.Column(db.Integer)

    def __str__(self):
        return f"Timeslot {self.start_time}"

    def get_occupied_capacity(self):
        return len(list([b for b in self.bookings if b.ack_at]))

    def get_free_capacity(self):
        return self.capacity - len(list([b for b in self.bookings if b.ack_at]))

    def has_free_capacity(self):
        return self.get_free_capacity() > 0
