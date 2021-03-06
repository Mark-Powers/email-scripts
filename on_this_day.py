import requests

from datetime import date
from bs4 import BeautifulSoup

from config import config

def check_error(func, name):
    try:
        return func()
    except:
        return "Error getting %s" % name

def get_on_this_day():
    old_news = check_error(get_old_news, "old news")
    peanuts = check_error(get_peanuts, "peanuts")
    calvin_and_hobbes = check_error(get_calvin_and_hobbes, "calvin and hobbes")
    wikipedia = check_error(get_today_wikipedia, "wikipedia")
    wikiquote = check_error(get_today_wikiquote, "wikiquote")
    thoreau = check_error(get_thoreau, "thoreau")

    return "<h1>On this day</h1><ul><li>%s</li><li>%s</li><li>%s</li><li>%s</li></ul><div>%s</div><div><pre>%s</pre></div>" % (old_news, peanuts, calvin_and_hobbes, wikipedia, wikiquote, thoreau)

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

def get_peanuts():
    print("getting peanuts")
    comic_date = date.today().strftime("%Y/%m/%d")
    full_url = "https://www.gocomics.com/peanuts/%s" % comic_date
    r = requests.get(full_url)
    soup = BeautifulSoup(r.text, features="lxml")
    comic_src = soup.select(".item-comic-image")[0].img["src"]
    return '<div><a href="%s">Peanuts</a></div>' % (comic_src)

def get_thoreau():
    print("getting thoreau")
    year_int = int(date.today().strftime("%Y")) - 183
    year = str(year_int)
    year_stop = str(year_int+1)
    month_day1 = date.today().strftime("_%b %-d._")
    month_day2 = date.today().strftime("_%b. %-d._")
    filename = config["thoreau"]["journal1"]
    with open(filename) as f:
        lines = f.readlines()

        # Find lines that the year lies on
        i= 0
        year_start_idx = -1
        for i in range(len(lines)):
            if lines[i].startswith(year):
                year_start_idx = i+1
                break
        year_stop_idx = -1
        for i in range(year_start_idx, len(lines)):
            if lines[i].startswith(year_stop):
                year_stop_idx = i - 2
                break
        entry_start_idx = -1

        # Find the lines inside the year that the date lies on
        i = year_start_idx
        while i < year_stop_idx:
            if lines[i].startswith(month_day1) or lines[i].startswith(month_day2):
                entry_start_idx = i - 2
                i += 1
                break
            i += 1
        entry_end_idx = -1
        while i < year_stop_idx:
            if lines[i].startswith("_"):
                entry_end_idx = i - 2
                break
            i += 1

        # If found date, join the strings
        if entry_start_idx != -1 and entry_end_idx != -1:
            return "".join(lines[entry_start_idx:entry_end_idx])
        return "No Thoreau entry on " + month_day1 + year
