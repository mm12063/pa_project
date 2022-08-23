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


file1 = open("MultiReg_RSA_MACD_Adj_OutScaled.txt", "a")
startdate = pd.to_datetime('2014-11-13')
enddate = pd.to_datetime('2019-12-31')
stocks = ['ALB', 'LAC', 'SQM', 'CBAT', 'ENS', '002466.SZ']
for stock in stocks:
	print(" [The current Stock : "+stock+" ] ")
	df = data.DataReader(stock, 'yahoo', startdate, enddate)
	#print(df.head(30))
	df.ta.macd(close='Adj Close', fast=12, slow=26, signal=9, append=True)
	#print(df.head(30))
	df.ta.rsi(close='Adj Close', fast=12, slow=26, signal=9, append=True)
	#print(df.head(30))
	#print(" [ After Reindexing ]")
	df = df.iloc[33:]
	
	ndf = df[['Adj Close','RSI_14','MACDs_12_26_9']]
	#print(ndf.head(30))
	#ndf.rename({'RSI_14': 'RSI','MACDs_12_26_9': 'MACD'}, axis=1, inplace=True)
	
	scaler = MinMaxScaler(feature_range=(0,1))
	scaled_data = ndf
	scaled_data[['Adj Close']] = scaler.fit_transform(scaled_data[['Adj Close']]) 
	#print(ndf.head(10))
	scaled_data[['RSI_14']] = scaler.fit_transform(scaled_data[['RSI_14']]) 
	#print(ndf.head(10))
	scaled_data[['MACDs_12_26_9']] = scaler.fit_transform(scaled_data[['MACDs_12_26_9']]) 
	#print(ndf.head(10))
	
	x = ndf[['RSI_14','MACDs_12_26_9']]
	y = ndf['Adj Close']
	
	X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=.2)
	model = LinearRegression()
	model.fit(X_train, y_train)
	y_pred = model.predict(X_test)
	
	mse = mean_squared_error(y_test, y_pred)
	rmse = math.sqrt(mse)
	mae = mean_absolute_error(y_test, y_pred)
	mape = mean_absolute_percentage_error(y_test, y_pred)

	
	
	print("The MAPE using RSI and MACD for ["+stock+"]: ",mape)
	print("The MAE using RSI and MACD for ["+stock+"]: ",mae)
	print("The RMSE using RSI and MACD for ["+stock+"]: ",rmse)
	print("The Coefficient of Determination using RSI and MACD for ["+stock+"]: ",r2_score(y_test, y_pred))
	print("\n")

	file1.write("\n\n")
	file1.write(" ["+stock+"] ")
	file1.write("\n\n")
	file1.write("The MAE using RSI and MACD for ["+stock+"]: "+str(mae)+"\n")
	file1.write("The MAPE using RSI and MACD for ["+stock+"]: "+str(mape)+"\n")
	file1.write("The RMSE using RSI and MACD for ["+stock+"]: "+str(rmse)+"\n")
	file1.write("The Coefficient of Determination for ["+stock+"]: "+str(r2_score(y_test, y_pred))+"\n")
	file1.write("\n\n")

file1.close()
