import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import current_app


def send_mail(to: list[str], subject: str, body: str):
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = f"Impfaktion Stadecken-Elsheim <{current_app.config.get('MAIL_SENDER')}>"
    message['Sender'] = f"Gemeinde Stadecken-Elsheim <{current_app.config.get('MAIL_SENDER')}>"
    message['To'] = ",".join(to)
    message['Return-Path'] = current_app.config.get('MAIL_REPLY_TO')
    message['Reply-To'] = current_app.config.get('MAIL_REPLY_TO')
    message.attach(MIMEText(body, "html"))
    msg_body = message.as_string()

    rcpt = to

    if current_app.config.get('MAIL_HOST') and not current_app.config.get('DEBUG'):
        with smtplib.SMTP(current_app.config.get('MAIL_HOST'), 25) as server:
            server.login(current_app.config.get('MAIL_USER'), current_app.config.get('MAIL_PASSWORD'))
            server.sendmail(current_app.config.get('MAIL_SENDER'), rcpt, msg_body)
    else:
        print(to)
        print(msg_body)


