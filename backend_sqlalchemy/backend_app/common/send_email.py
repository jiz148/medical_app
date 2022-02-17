"""
Email Sender
"""
import smtplib
from email.mime.text import MIMEText


def send_email(sender, password, receiver, subject, content, smtp_server, port):

    msg = MIMEText(content)
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject

    if port == '465':
        server = smtplib.SMTP_SSL('{}:{}'.format(smtp_server, port))
    else:
        server = smtplib.SMTP('{}:{}'.format(smtp_server, port))
        server.starttls()  # this is for secure reason

    server.login(sender, password)
    server.send_message(msg)
    server.quit()
