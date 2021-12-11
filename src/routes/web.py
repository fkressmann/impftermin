from flask import Blueprint, render_template, request

from extensions.db import db
from models.Timeslot import Timeslot
from models.Booking import Booking
from requests.Reservation import Reservation

web_bp = Blueprint('web', __name__)


@web_bp.route('/')
def index():
    timeslots: [Timeslot] = Timeslot.query.all()
    return render_template('index.html', timeslots=timeslots)


@web_bp.route('/reservation', methods=['POST'])
def reservation():
    r = Reservation(request.form)
    if r.valid:
        if not r.timeslot.has_free_capacity():
            return "Timeslot is fully booked", 418

        booking = Booking(name=r.name,
                          email=r.email,
                          timeslot=r.timeslot)
        print(f"Free:{r.timeslot.get_free_capacity()}")
        db.session.add(booking)
        db.session.commit()
        return "success!", 200
    else:
        return "Invalid request!", 400

