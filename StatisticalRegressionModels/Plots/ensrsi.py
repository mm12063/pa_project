import yfinance as yf
import math
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from pandas_datareader import data,wb
import pandas_ta
from datetime import date
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error, mean_absolute_error
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import statsmodels.api as sm
pd.options.mode.chained_assignment = None  # default='warn'

startdate = pd.to_datetime('2014-12-11')
enddate = pd.to_datetime('2019-12-31')
stock = 'ENS'

print(" [The current Stock : ",stock," ] ")
df = data.DataReader(stock, 'yahoo', startdate, enddate)
df.ta.rsi(close='Close', fast=12, slow=26, signal=9, append=True)
df = df.iloc[14:]
#df['Date'] = pd.to_datetime(df['Date']) 
#df = df.set_index('Date')
#print(df)
plt.title(stock+" Graph")
plt.xlabel('Days')
plt.ylabel('Price')
plt.plot(df.index,df['Close'], label='Closing Prices')
plt.plot(df.index, df['RSI_14'], label='RSI')
plt.legend()
plt.show()