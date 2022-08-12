import pandas as pd
from os.path import exists
import re

loc = "data/csv/"

sources = [
    'bloom',
    'ft',
    'reuters',
]

names = [
    # 'albemarle',
    # 'ganfeng_lithium',
    # 'sqm',
    'sociedad_quimica_y_minera_de_chile',
    # 'lithium',
]

for name in names:
    temp_df = pd.DataFrame()
    headlines = []
    dates = []
    snippets = []

    for source in sources:
        filename = source+"_"+name
        path_to_file = loc + filename + '.csv'
        if exists(path_to_file):
            file_data = pd.read_csv(path_to_file)
            for index, row in file_data.iterrows():
                name_sep = name.replace("_", " ")
                headline = str(row['headline']).lower()
                snippet = str(row['snippet']).lower()
                if name_sep in headline or name_sep in snippet:
                    headlines.append(row['headline'])
                    snippets.append(row['snippet'])
                    dates.append(row['date'])
        df = pd.DataFrame({'headline': headlines, 'date': dates, 'snippet': snippets,'source': source})
        temp_df = pd.concat([temp_df, df])

    print(temp_df.to_string())

    loc = "data/csv/compiled/" + name + "_for_snippet_analysis.csv"
    temp_df.to_csv(loc, ",")

