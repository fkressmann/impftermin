import uuid

from extensions.db import db


class Timeslot(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Activity {self.name}>"