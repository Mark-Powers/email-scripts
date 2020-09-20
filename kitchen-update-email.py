import smtplib
from email.mime.text import MIMEText 
from email.utils import formatdate
import pymysql
import sys

import email_helper
from config import config

def get_last_sent_update(cursor):
    cursor.execute("SELECT last_update FROM updates;")
    return cursor.fetchone()[0]

def get_later_post(cursor, last):
    cursor.execute("SELECT id,type  FROM posts where id > " + str(last) +" ORDER BY id asc")
    return cursor.fetchone()

def set_last_sent_update(cursor, db, post_id):
    cursor.execute("UPDATE updates SET last_update=" + str(post_id)+ " where id=1")
    db.commit()

def get_emails(cursor):
    cursor.execute("SELECT name, address FROM emails")
    return cursor.fetchall()

def add_update(cursor, db, post_id):
    cursor.execute("insert into updates values (1, " +str(post_id)+", NOW())")
    db.commit()

def handle_update():
    """ Check for a new post on my website and email everyone on the list
    if there is one.
    """

    db = pymysql.connect("localhost", config["database"]["user"], config["database"]["pass"], config["database"]["db"])
    cursor = db.cursor()

    last = get_last_sent_update(cursor)

    new_post = get_later_post(cursor, last)
    if not new_post:
        print("no new post")
        sys.exit()
    if new_post[1] == 'index':
        print("ignoring index post")
        sys.exit()
    print(new_post)

    set_last_sent_update(cursor, db, new_post[0])
    emails = get_emails(cursor)

    name = config["email"]["name"]
    frm = config["email"]["user"]
    subject = "marks.kitchen update"
    for email in emails:
        to = email[1]
        body = """
    Hi """ + email[0] + """!

    There is a new post on marks.kitchen! Check it out: https://marks.kitchen/post/"""+new_post[1]+"""/"""+str(new_post[0])+"""

    Mark (mark@marks.kitchen)
    """
        email_helper.send(frm, name, to, subject, body)
    add_update(cursor, db, new_post[0])
    db.close()

if __name__ == "__main__":
    handle_update()

