#!/usr/bin/python3

import requests

from datetime import date
from bs4 import BeautifulSoup
from email.mime.text import MIMEText 
from email.utils import formatdate

import on_this_day
import email_helper
from config import config

def get_weather():
    print("getting weather")
    weather_url = "https://forecast.weather.gov/MapClick.php?lon=%s&lat=%s" % (config["weather"]["lon"], config["weather"]["lat"])
    soup = BeautifulSoup(requests.get(weather_url).text, features="lxml")
    return str(soup.select("#detailed-forecast")[0])

def get_unread_reminders():
    print("getting unread reminders")
    subjects = email_helper.filter_unread("subject", "REMINDER:", "subject")
    subjects = [s["subject"][len("REMINDER: "):].strip() for s in subjects]
    if len(subjects) > 0:
        reminder_html = "<h1>Reminders:</h1><ul>"
        for s in subjects:
            reminder_html += "<li>%s</li>" % s
        reminder_html += "</ul>\n"
        return reminder_html
    return ""

def format_email():
    print("forming email")
    return '%s%s%s' % (get_unread_reminders(), on_this_day.get_on_this_day(), get_weather())

def send_update_email():
    frm = config["email"]["user"]
    name = config["email"]["name"]
    
    today = date.today().strftime("%b %d")
    subject = "Updates for " + today

    body = format_email()
    email_helper.send(frm, name, frm, subject, body, "html")

if __name__ == "__main__":
    send_update_email()

