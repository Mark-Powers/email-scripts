#!/usr/bin/python3

import email_helper
import datetime
import subprocess
from config import config

def get_wiki_emails():
    bodies = email_helper.filter_unread("subject", "TODAY", "body date")
    for b in bodies:
        d = datetime.datetime.strptime(b["date"], "%a, %d %b %Y %H:%M:%S %z")
        title = d.strftime("%B %-d")
        path = d.strftime("%Y/%b/%d").lower()
        exe = "/home/mark/projects/wikijscmd/main.py"
        args = [exe, "create", path, title, b["body"]]
        print(args)
        subprocess.run(args)

get_wiki_emails()
