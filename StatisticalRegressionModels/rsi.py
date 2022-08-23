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
pd.options.mode.chained_assignment = None  # default='warn'

file1 = open("RSI_14_Out.txt", "a")
startdate = pd.to_datetime('2014-12-11')
enddate = pd.to_datetime('2019-12-31')
stocks = ['ALB', 'LAC', 'SQM', 'CBAT', 'ENS', '002466.SZ']

for stock in stocks:
	print(" [The current Stock : "+stock+" ] ")
	df = data.DataReader("ENS", 'yahoo', startdate, enddate)
	df.ta.rsi(close='close', fast=12, slow=26, signal=9, append=True)
	df = df.iloc[14:]
	#print(df.head(10))

	scaler = MinMaxScaler(feature_range=(0,1))
	scaled_data = df
	scaled_data[['Close', 'RSI_14']] = scaler.fit_transform(scaled_data[['Close', 'RSI_14']]) 

	X_train, X_test, y_train, y_test = train_test_split(scaled_data[['Close']], scaled_data[['RSI_14']], test_size=.2)

	model = LinearRegression()
	model.fit(X_train, y_train)
	y_pred = model.predict(X_test)

	mse = mean_squared_error(y_test, y_pred)
	rmse = math.sqrt(mse)
	mae = mean_absolute_error(y_test, y_pred)
	mape = mean_absolute_percentage_error(y_test, y_pred)

	print("The MAPE using RSI_14 for ["+stock+"]: ",mape)
	print("The MAE using RSI_14 for ["+stock+"]: ",mae)
	print("The RMSE using RSI_14 for ["+stock+"]: ",rmse)
	print("The Coefficient of Determination using RSI_14 for ["+stock+"]: ",r2_score(y_test, y_pred),"\n")

	file1.write("\n\n")
	file1.write(" ["+stock+"] ")
	file1.write("\n\n")
	file1.write("MAE using RSI_14 for ["+stock+"]: "+str(mae)+"\n")
	file1.write("MAPE using RSI_14 for ["+stock+"]: "+str(mape)+"\n")
	file1.write("RMSE using RSI_14 for ["+stock+"]: "+str(rmse)+"\n")
	file1.write("Coefficient of Determination using RSI_14 for ["+stock+"]: "+str(r2_score(y_test, y_pred))+"\n")
	file1.write("\n\n")

file1.close()
