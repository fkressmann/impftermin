import datetime

from flask import Blueprint, render_template, request

from extensions.db import db
from models.Timeslot import Timeslot
from models.Booking import Booking
from requests.Reservation import Reservation
from services.mail_service import send_mail
from util import *

web_bp = Blueprint('web', __name__)


@web_bp.route('/')
def index():
    timeslots: [Timeslot] = Timeslot.query.order_by(Timeslot.start_time).all()
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

        db.session.add(booking)
        db.session.commit()
        send_mail([booking.email],
                  "Terminanfrage Impfaktion Stadecken-Elsheim",
                  render_template("email.html", reservation=booking))
        return render_template("reservation.html", reservation=booking), 200
    else:
        return "Invalid request!", 400


@web_bp.route('/confirm')
def confirm():
    maybe_booking: Booking = Booking.query.get(request.args.get("id"))
    if not maybe_booking:
        return "Reservation not found", 404

    if not maybe_booking.ack_at:
        maybe_booking.ack_at = datetime.datetime.now()
    db.session.commit()
    return render_template("confirmation.html", reservation=maybe_booking)


@web_bp.route('/admin-6a3522f3-6c6e-4b0e-a044-d653177fbb91')
def admin():
    timeslots = Timeslot.query.order_by(Timeslot.start_time).all()
    return render_template("admin.html", timeslots=timeslots)


@web_bp.route('/admin-create-6a3522f3-6c6e-4b0e-a044-d653177fbb91', methods=['POST'])
def admin_create():
    r = Reservation(request.form)
    if r.valid:
        booking = Booking(name=r.name,
                          email=r.email,
                          timeslot=r.timeslot,
                          ack_at=datetime.datetime.now())
        db.session.add(booking)
        db.session.commit()

        return redirect(url_for('web.admin'))
    else:
        return "Invalid request!", 400


@web_bp.route('/delete')
def delete():
    maybe_booking: Booking = Booking.query.get(request.args.get("id"))
    if not maybe_booking:
        return "Reservation not found", 404
    else:
        db.session.delete(maybe_booking)
        db.session.commit()
    return render_template("confirmation-deleted.html")
