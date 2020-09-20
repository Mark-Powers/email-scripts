#!/usr/bin/python3

import smtplib
import sys
import time
import requests

from datetime import date
from bs4 import BeautifulSoup
from email.mime.text import MIMEText 
from email.utils import formatdate

import email_helper
from config import config

def get_weather():
    print("getting weather")
    weather_url = "https://forecast.weather.gov/MapClick.php?lon=%s&lat=%s" % (config["weather"]["lon"], config["weather"]["lat"])
    soup = BeautifulSoup(requests.get(weather_url).text, features="lxml")
    return str(soup.select("#detailed-forecast")[0])

def get_old_news():
    print("getting old news")
    year = int(date.today().strftime("%Y")) - 100
    century_ago = str(year) + date.today().strftime("-%m-%d")
    news_text = ""
    urls = config["news"]["urls"].split(",")
    names = config["news"]["names"].split(",")
    for i in range(len(urls)):
        full_url = urls[i] % century_ago
        name = names[i]
        if requests.get(full_url).status_code != 404:
            news_text += '<a href="%s">%s %s</a>\n' % (full, name, century_ago)
    return news_text

def get_unread_reminders():
    print("getting unread reminders")
    subjects = email_helper.filter_unread("subject", "REMINDER:", "subject")
    subjects = [s[len("REMINDER: "):].strip() for s in subjects]
    if len(subjects) > 0:
        reminder_html = "<h1>Reminders:</h1><ul>"
        for s in subjects:
            reminder_html += "<li>%s</li>" % s
        reminder_html += "</ul>\n"
        return reminder_html
    return ""

def format_email():
    print("forming email")
    return '%s%s%s' % (get_unread_reminders(), get_old_news(), get_weather())

def send_update_email():
    frm = config["email"]["user"]
    name = config["email"]["name"]
    
    today = date.today().strftime("%b %d")
    subject = "Updates for " + today

    body = format_email()
    email_helper.send(frm, name, frm, subject, body, "html")

if __name__ == "__main__":
    send_update_email()

