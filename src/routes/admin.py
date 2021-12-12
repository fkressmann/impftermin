import datetime

from flask import Blueprint, render_template, request, current_app

from extensions.db import db
from models.Timeslot import Timeslot
from models.Booking import Booking
from requests.Reservation import Reservation
from services.mail_service import send_mail
from util import *

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin-6a3522f3-6c6e-4b0e-a044-d653177fbb91')
def index():
    timeslots = Timeslot.query.order_by(Timeslot.start_time).all()
    return render_template("admin.html", timeslots=timeslots)


@admin_bp.route('/admin-create-6a3522f3-6c6e-4b0e-a044-d653177fbb91', methods=['POST'])
def create():
    r = Reservation(request.form)
    if r.is_valid_admin_request():
        booking = Booking(name=r.name,
                          email=r.email,
                          timeslot=r.timeslot,
                          vaccination=r.vaccination,
                          age=r.age,
                          ack_at=datetime.datetime.now())
        db.session.add(booking)
        db.session.commit()

        return redirect(url_for('.index'))
    else:
        return "Invalid request!", 400
