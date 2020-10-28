import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.utils import formatdate
from email.header import decode_header

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

def get_subject(msg):
    subject = decode_header(msg["Subject"])[0][0]
    if isinstance(subject, bytes):
        subject = subject.decode()
    return subject

def get_body(msg):
    if msg.is_multipart():
        body = ""
        for part in msg.walk():
            try:
                # get the email body
                body += part.get_payload(decode=True).decode()
            except:
                pass
    else:
        body = msg.get_payload(decode=True).decode()
    return body

def get_from(msg):
    return msg.get("From")

def get_date(msg):
    return msg.get("Date")

def get_content_type(msg):
    return msg.get_content_type()

def set_unseen(imap, idx):
    imap.store(idx, '-FLAGS', '\\SEEN')

def get_what(msg, what):
    ret = {}
    if "subject" in what:
        ret["subject"] = get_subject(msg)
    if "body" in what:
        ret["body"] = get_body(msg)
    if "from" in what:
        ret["from"] = get_from(msg)
    if "content_type" in what:
        ret["content_type"] = get_content_type(msg)
    if "date" in what:
        ret["date"] = get_date(msg)
    return ret

def parse(imap, index, check_what, criteria, return_what):
    res, msg = imap.fetch(index, "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            if criteria in get_what(msg, check_what)[check_what]:
                return get_what(msg, return_what)

def filter_unread(check_what, criteria, return_what):
    """ check if the field 'check_what' contains the given criteria, and if so return a list
    of the field 'return_what'
    """
    imap = imaplib.IMAP4_SSL(config["email"]["server"])
    imap.login(config["email"]["user"], config["email"]["pass"])
    status, messages = imap.select("INBOX")
    
    status, response = imap.search(None, '(UNSEEN)')
    unread_msg_nums = response[0].split()

    ret = [] 
    for i in unread_msg_nums:
        parse_return = parse(imap, i, check_what, criteria, return_what)
        if parse_return is not None:
            ret.append(parse_return)
        set_unseen(imap, i)
    imap.close()
    imap.logout()

    return ret

