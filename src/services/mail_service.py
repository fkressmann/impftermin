import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import current_app


def send_mail(to, bcc, subject, body):
    to = [current_app.config.get('MAIL_REPLY_TO')] if current_app.debug else to

    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = f"Gemeinde Stadecken-Elsheim <{current_app.config.get('MAIL_SENDER')}>"
    message['To'] = ",".join(to)
    message['Reply-To'] = current_app.config.get('MAIL_REPLY_TO')
    message.attach(MIMEText(body, "html"))
    msg_body = message.as_string()

    rcpt = to + bcc

    if current_app.config.get('MAIL_HOST'):
        with smtplib.SMTP(current_app.config.get('MAIL_HOST'), 25) as server:
            server.sendmail(current_app.config.get('MAIL_SENDER'), rcpt, msg_body)
    else:
        print(to)
        print(bcc)
        print(msg_body)


