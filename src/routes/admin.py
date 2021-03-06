import datetime

from flask import Blueprint, render_template, request
from sqlalchemy.exc import IntegrityError

from extensions.db import db
from models.Timeslot import Timeslot
from models.Booking import Booking
from requests.Reservation import Reservation
from util import *

admin_bp = Blueprint('admin', __name__)

# Yep this will be changed before the next deployment :D
admin_hidden_link = '6a3522f3-6c6e-4b0e-a044-d653177fbb91'


@admin_bp.route(f"/admin-{admin_hidden_link}")
def index():
    timeslots = Timeslot.query.order_by(Timeslot.start_time).all()
    return render_template("admin.html", timeslots=timeslots)


@admin_bp.route(f"/admin-create-{admin_hidden_link}", methods=['POST'])
def create():
    r = Reservation(request.form)
    if r.is_valid_admin_request():
        booking = Booking(name=r.name,
                          email=r.email,
                          timeslot=r.timeslot,
                          vaccination=r.vaccination,
                          age=r.age,
                          ack_at=datetime.datetime.now())
        try:
            db.session.add(booking)
            db.session.commit()
        except IntegrityError:
            return render_template("email-duplicated.html")

        return redirect(url_for('.index'))
    else:
        return "Invalid request!", 400


@admin_bp.route(f"/admin-print-{admin_hidden_link}")
def print_bookings():
    timeslots = Timeslot.query.order_by(Timeslot.start_time).all()
    return render_template("admin-print.html", timeslots=timeslots)
