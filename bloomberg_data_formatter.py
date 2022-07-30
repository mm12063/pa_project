import pandas as pd
from bs4 import BeautifulSoup
import datetime
import globals

filenames = [
    'bloom_ganfeng_lithium',
    'bloom_albemarle',
    # 'bloom_lithium',
    'bloom_sqm',
    ]

for filename in filenames:
    soup = BeautifulSoup(open("data/html/"+filename+".html"), "html.parser")

    headlines = soup.find_all('a', {'class': 'headline__96ba1917df'})
    dates = soup.find_all('div', {'class': 'publishedAt__aa20732e3f'})
    snippet = soup.find_all('a', {'class': 'summary__f7259c7b77'})

    formatted_headlines = []
    formatted_dates = []
    cleaned_snippets = []

    for i in range(len(headlines)):
        date = dates[i].find_next(text=True).strip()
        date = date.replace(",","",1)
        dt = datetime.datetime.strptime(date.replace(",", "", 1), '%B %d %Y').strftime('%d/%m/%Y')

        temp_day, temp_month, temp_year = globals.get_date_parts(dt)

        if (globals.date_range_st <= datetime.date(temp_year, temp_month, temp_day) <= globals.date_range_end):
            formatted_dates.append(dt)

            headline = headlines[i].find_next(text=True).string.strip()
            formatted_headlines.append(headline)

            if (i < len(snippet)):
                cleaned_snippets.append(snippet[i].text.strip('"'))
            else:
                cleaned_snippets.append('')

    data_nbc = pd.DataFrame({'headline': formatted_headlines, 'date': formatted_dates, 'snippet': cleaned_snippets, 'source': 'bloomberg'})
    print(data_nbc.head())

    loc = "data/csv/"+filename+".csv"
    data_nbc.to_csv(loc, ",")
