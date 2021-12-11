import uuid

from extensions.db import db


class Timeslot(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    capacity = db.Column(db.Integer)

    def __repr__(self):
        return f"<Activity {self.name}>"

    def get_free_capacity(self):
        return self.capacity - len(list([b for b in self.bookings if b.ack_at]))

    def get_free(self):
         return next(db.engine.execute(
            f"select capacity - (select count(*) from booking where ack_at is not null and timeslot_id = '{self.id}') from timeslot where id = '{self.id}';"))[0]
