import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

from config import config

def send(frm, name, to, subject, body, subtype="plain"):
    """Send a email to the given address, from the given address and name with the subject and body 
    """
    try:
        server = smtplib.SMTP(config["email"]["server"], int(config["email"]["port"]))
        server.ehlo()
        server.starttls()
        server.login(config["email"]["user"], config["email"]["pass"])

        frm = "%s <%s>" % (name, frm)
        e = MIMEText(body, subtype)
        e['Subject'] = subject
        e['From'] = frm
        e['To'] = to 
        e.add_header('Date', formatdate())

        server.sendmail(frm, to, e.as_string())

    except Exception as e:
        print("error")
        print(e)

