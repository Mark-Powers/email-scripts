import requests

from datetime import date
from bs4 import BeautifulSoup

from config import config

def get_on_this_day():
    return "<h1>On this day</h1>%s%s%s%s" % (get_old_news(), get_calvin_and_hobbes(), get_today_wikipedia(), get_today_wikiquote())

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
            news_text += '<div><a href="%s">%s %s</a></div>\n' % (full_url, name, century_ago)
    return news_text

def get_today_wikipedia():
    print("getting today's wikipedia")
    full_url = "https://en.wikipedia.org/wiki/%s" % date.today().strftime("%B_%d")
    return '<div><a href="%s">Today\'s Wikipedia</a></div>' % (full_url)

def get_today_wikiquote():
    print("getting today's wikiquote")
    full_url = "https://en.wikiquote.org/wiki/%s" % date.today().strftime("%B_%d")
    r = requests.get(full_url)
    soup = BeautifulSoup(r.text, features="lxml")
    table = str(soup.find(text="2020").parent.parent.next_sibling.next_sibling)
    table = table.replace('href="/', 'href="https://en.wikiquote.org/')
    return '<div style="border: 1px solid black">%s</div>' % table

def get_calvin_and_hobbes():
    print("getting calvin and hobbes")
    year = int(date.today().strftime("%Y")) % 9 + 1986
    comic_date = str(year) + date.today().strftime("/%m/%d")
    full_url = "https://www.gocomics.com/calvinandhobbes/%s" % comic_date
    r = requests.get(full_url)
    soup = BeautifulSoup(r.text, features="lxml")
    if not "Today on" in str(soup.title): # gocomics gives you today if 404
        comic_src = soup.select(".item-comic-image")[0].img["src"]
        return '<div><a href="%s">Calvin and Hobbes</a></div>' % (comic_src)
    else:
        return ""
