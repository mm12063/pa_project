import pandas as pd
from bs4 import BeautifulSoup
import datetime
import globals

filenames = [
    'ft_ganfeng_lithium',
    'ft_albemarle',
    'ft_lithium',
    'ft_sqm',
    ]

for filename in filenames:
    soup = BeautifulSoup(open("data/html/"+filename+".html"), "html.parser")

    headlines = soup.find_all('h2', {'class': 'title'})
    dates = soup.find_all('span', {'class': 'issue_date'})
    snippet = soup.find_all('div', {'class': 'text-snippet'})

    formatted_headlines = []
    formatted_dates = []
    cleaned_snippets = []

    for i in range(len(headlines)):
        date = dates[i].find_next(text=True).strip()
        date = date.replace(",","",1)
        dt = datetime.datetime.strptime(date.replace(",", "", 1), '%A %B %d %Y').strftime('%d/%m/%Y')

        temp_day, temp_month, temp_year = globals.get_date_parts(dt)

        if (globals.date_range_st <= datetime.date(temp_year, temp_month, temp_day) <= globals.date_range_end):
            formatted_dates.append(dt)

            headline = headlines[i].find_next(text=True).strip()
            formatted_headlines.append(headline)

            if (i < len(snippet)):
                for snip in snippet[i].findAll('p'):
                    if snip.parent.name == 'div':
                        cleaned_snippets.append(snip.text.replace("\"","",1).strip())
            else:
                cleaned_snippets.append('')

    data_nbc = pd.DataFrame({'headline': formatted_headlines, 'date': formatted_dates, 'snippet': cleaned_snippets, 'source': 'ft'})
    print(data_nbc.head())

    loc = "data/csv/"+filename+".csv"
    data_nbc.to_csv(loc, ",")
