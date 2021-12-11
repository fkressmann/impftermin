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
    return Timeslot.query.all(), 200

