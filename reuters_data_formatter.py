import pandas as pd
from bs4 import BeautifulSoup
import datetime
from fake_user_agent.main import user_agent
import json
from io import StringIO
from html.parser import HTMLParser
import globals
import time
from urllib.error import HTTPError, URLError
import urllib.request
import re

source = 'reuters'
pg_st = 0
pg_end = 1

def make_request(url):
    ua = user_agent()
    headers = {
        'User-Agent': ua
    }
    req = urllib.request.Request(url, data=None, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read(), response
    except HTTPError as error:
        print(error.status, error.reason)
    except URLError as error:
        print(error.reason)
    except TimeoutError:
        print("Request timed out")


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def clean_data_pre_json(data, name):
    splitter = "addMoreNewsResults( "
    data = data.split(splitter, 1)[-1].rsplit(');', 1)[0]
    data = data \
        .replace("'"+name+"',", '"'+name+'",') \
        .replace("'date',", '"date",') \
        .replace(" id:", 'article_id:') \
        .replace("'all',", '"all",')

    for key in keys:
        data = data.replace(key + ":", '"' + key + '":')

    return data


def convert_to_json(text, name):
    data = clean_data_pre_json(text, name)
    try:
        return json.loads(data)
    except:
        print("Can't convert to JSON:")
        print(data)
    return


def clean_text(str):
    str = str.strip("...").replace("\n", "").replace("...", "").replace('"', "\"").strip().rstrip()
    str = re.sub('\\s+', ' ', str)
    return strip_tags(str)


def is_update(str):
    if str[0:6] == "UPDATE" and str[8:9] == "-":
        return True
    else:
        return False


def convert_to_DMY(date):
    date = date.strip()[:-12]
    return datetime.datetime.strptime(date.replace(",", "", 1), '%B %d %Y').strftime('%d/%m/%Y')


ua = user_agent()
headers = {'User-Agent': ua}

keys = [
    "blob",
    "sortBy",
    "dateRange",
    "totalResultNumber",
    "totalResultNumberStr",
    "news",
    "article_id",
    "headline",
    "date",
    "href",
    "blurb",
    "mainPicUrl",
]

names = [
    # 'ganfeng+lithium',
    # 'albemarle',
    'sociedad+quimica+y+minera+de+chile',
    # 'sqm',
    # 'lithium',
    ]

for name in names:
    url = 'https://www.reuters.com/assets/searchArticleLoadMoreJson?blob=' + name + '&bigOrSmall=big&articleWithBlog=true&sortBy=date&dateRange=all&numResultsToShow=100&callback=addMoreNewsResults&pn='

    formatted_headlines = []
    formatted_dates = []
    cleaned_snippets = []

    for page_num in range(pg_st,pg_end):
        print("name:", name)

        print("page_num:",page_num)
        print("Headlines count:",len(formatted_headlines))

        url_updated = url + str(page_num)
        print(url_updated)

        text, response = make_request(url_updated)
        print("Txt len", len(text))
        soup = BeautifulSoup(text, features="lxml")

        data = convert_to_json(soup.text, name)

        for i, news in enumerate(data['news']):
            headline = clean_text(news['headline'])
            date = clean_text(news['date'])
            blurb = clean_text(news['blurb'])

            dt = convert_to_DMY(date)
            temp_day, temp_month, temp_year = globals.get_date_parts(dt)

            if (globals.date_range_st <= datetime.date(temp_year, temp_month, temp_day) <= globals.date_range_end):
                if headline not in formatted_headlines and is_update(headline) is False:
                    formatted_headlines.append(headline)
                    cleaned_snippets.append(blurb)
                    formatted_dates.append(dt)

        time.sleep(2)

    df = pd.DataFrame({'headline': formatted_headlines, 'date': formatted_dates, 'snippet': cleaned_snippets,
                             'source': source})
    print(df.head())

    filename = source+"_"+name.replace("+", "_").lower()
    loc = "data/csv/" + filename + ".csv"
    df.to_csv(loc, ",")
    print(len(df.index), "rows")
