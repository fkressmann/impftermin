import datetime

from flask import Blueprint, render_template, request, current_app
from sqlalchemy.exc import IntegrityError

from extensions.db import db
from models.Timeslot import Timeslot
from models.Booking import Booking
from requests.Reservation import Reservation
from services.mail_service import send_mail

web_bp = Blueprint('web', __name__)


@web_bp.before_request
def is_registration_open():
    if datetime.datetime.now() < current_app.config.get("START_TIME"):
        return render_template("index-not-started.html", start=current_app.config.get("START_TIME"))
    elif datetime.datetime.now() > current_app.config.get("CLOSING_TIME"):
        return render_template("index-ended.html", end=current_app.config.get("CLOSING_TIME"))


@web_bp.route('/')
def index():
    timeslots: [Timeslot] = Timeslot.query.order_by(Timeslot.start_time).all()
    return render_template('index.html', timeslots=timeslots, end=current_app.config.get("CLOSING_TIME"))


@web_bp.route('/reservation', methods=['POST'])
def reservation():
    r = Reservation(request.form)
    if r.is_valid_external_request():
        if not r.timeslot.has_free_capacity():
            return "Dieses Zeitfenster ist leider ausgebucht", 400

        booking = Booking(name=r.name,
                          email=r.email,
                          timeslot=r.timeslot,
                          vaccination=r.vaccination,
                          age=r.age)

        try:
            db.session.add(booking)
            db.session.commit()
        except IntegrityError:
            return render_template("email-duplicated.html")

        send_mail([booking.email],
                  "Terminanfrage Impfaktion Stadecken-Elsheim",
                  render_template("email.html", reservation=booking))
        return render_template("reservation.html", reservation=booking)
    else:
        return "Diese Anfrage ist nicht gültig, bitte kehren Sie zur vorherigen Seite zurück und überprüfen Ihre Angaben", 400


@web_bp.route('/confirm')
def confirm():
    maybe_booking: Booking = Booking.query.get(request.args.get("id"))
    if not maybe_booking:
        return render_template("confirmation-not-found.html")

    if not maybe_booking.ack_at and not maybe_booking.timeslot.has_free_capacity():
        db.session.delete(maybe_booking)
        db.session.commit()
        return render_template("confirmation-full.html")

    if not maybe_booking.ack_at:
        maybe_booking.ack_at = datetime.datetime.now()

    db.session.commit()
    return render_template("confirmation.html", reservation=maybe_booking)


@web_bp.route('/delete')
def delete():
    maybe_booking: Booking = Booking.query.get(request.args.get("id"))
    if not maybe_booking:
        return "Reservation not found", 404
    else:
        db.session.delete(maybe_booking)
        db.session.commit()
    return render_template("confirmation-deleted.html")


@web_bp.route('/dataprotection')
def dataprotection():
    return render_template('dataprotection.html')
