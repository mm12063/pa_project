import pandas as pd

"""
FILES:
main_ds_nlp.csv
merged_weather.csv

"""

r1 = pd.read_csv('main_ds_nlp.csv')
r2 = pd.read_csv('merged_weather.csv')

#print(r2.shape)
#print(r2.head())

r2.rename({'datetime': 'Date'}, axis=1, inplace=True)
#print(r2.shape)
#print(r2.head())

r2['Date'] = pd.to_datetime(r2.Date, format='%m/%d/%Y')
r2['Date'] = r2['Date'].dt.strftime('%d/%m/%Y')
#print(r2.shape)
#print(r2.head())

output = pd.merge(r1, r2, on='Date', how='inner')
output.to_csv('main_ds_nlp_weather.csv')