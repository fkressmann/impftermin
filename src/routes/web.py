from datetime import datetime, timedelta

from flask import Blueprint, session, get_flashed_messages, render_template, request, flash, current_app, jsonify
from sqlalchemy import func

from extensions.db import db
from models.Timeslot import Timeslot
from models.Booking import Booking
from routes.util import *

web_bp = Blueprint('web', __name__)


@web_bp.route('/')
def index():
    timeslots: [Timeslot] = Timeslot.query.all()
    return render_template('index.html', timeslots=timeslots)


@web_bp.route('/reservation', methods=['POST'])
def reservation():
    return request.form, 200

