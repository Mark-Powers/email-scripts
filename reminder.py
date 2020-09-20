import smtplib
from email.mime.text import MIMEText 
from email.utils import formatdate
import sys

import email_helper
from config import config

def send_reminder():
    """Sends a reminder email based on the arguments for easy scripting
    Usage: python3 reminder.py <subject> <body...>
    """

    name = config["email"]["name"]
    user = config["email"]["user"]
    subject = "REMINDER: %s" % sys.argv[1]
    body = sys.argv[2] if len(sys.argv) > 2 else ""
    email_helper.send(user, name, user, subject, body)

if __name__ == "__main__":
    send_reminder()
