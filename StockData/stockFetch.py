import pandas as pd
import pandas_datareader.data as web

stocks = ['ALB', 'SQM', 'LAC', 'ENS', 'CBAT', '002466.SZ']
data_source = 'yahoo'
start_date = '2021-08-01'
end_date = '2022-07-31'

for stock in stocks:
	stock_df = web.DataReader(stock, data_source, start_date, end_date)
	stock_df.to_csv(stock+'.csv')
