import pandas as pd
import pandas_datareader as pdr
import datetime as dt
import numpy as np
 
tickers = ['ENS', 'CBAT', '002466.SZ', 'ALB', 'LAC', 'SQM']
start = dt.datetime(2015, 1, 1)
end = dt.datetime(2019, 12, 31)
data = pdr.get_data_yahoo(tickers, start, end)
data = data['Close']
 
log_returns = np.log(data/data.shift())
print(log_returns.corr())