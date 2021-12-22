import os

from datetime import datetime

DB_HOST = os.environ.get("DB_HOST")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_USER = os.environ.get("DB_USER")
DB_NAME = os.environ.get("DB_NAME")
MAIL_HOST = os.environ.get("MAIL_HOST")
MAIL_SENDER = os.environ.get("MAIL_SENDER")
MAIL_USER = os.environ.get("MAIL_USER")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
MAIL_REPLY_TO = os.environ.get("MAIL_REPLY_TO")
CLOSING_TIME = datetime.fromisoformat(os.environ.get("CLOSING_TIME"))
START_TIME = datetime.fromisoformat(os.environ.get("START_TIME"))