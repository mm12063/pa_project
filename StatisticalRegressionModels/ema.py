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

file1 = open("EMA10_Out.txt", "a")
startdate = pd.to_datetime('2014-12-18')
enddate = pd.to_datetime('2019-12-31')
stocks = ['ALB', 'LAC', 'SQM', 'CBAT', 'ENS', '002466.SZ']

for stock in stocks:
	print(" [The current Stock : "+stock+" ] ")
	df = data.DataReader(stock, 'yahoo', startdate, enddate)
	df.ta.ema(close='Close', length=10, append=True)
	df = df.iloc[9:]
	#print(df.head(10))

	X_train, X_test, y_train, y_test = train_test_split(df[['Close']], df[['EMA_10']], test_size=.2)

	model = LinearRegression()
	model.fit(X_train, y_train)
	y_pred = model.predict(X_test)

	mse = mean_squared_error(y_test, y_pred)
	rmse = math.sqrt(mse)
	mae = mean_absolute_error(y_test, y_pred)
	mape = mean_absolute_percentage_error(y_test, y_pred)

	print("The MAPE using MACD for ["+stock+"]: ",mape)
	print("The MAE using MACD for ["+stock+"]: ",mae)
	print("The RMSE using MACD for ["+stock+"]: ",rmse)
	print("The Coefficient of Determination using : ",r2_score(y_test, y_pred),"\n")

	file1.write("\n\n")
	file1.write(" ["+stock+"] ")
	file1.write("\n\n")
	file1.write("The MAE using MACD for ["+stock+"]: "+str(mae)+"\n")
	file1.write("The MAPE using MACD for ["+stock+"]: "+str(mape)+"\n")
	file1.write("The RMSE using MACD for ["+stock+"]: "+str(rmse)+"\n")
	file1.write("The Coefficient of Determination for ["+stock+"]: "+str(r2_score(y_test, y_pred))+"\n")
	file1.write("\n\n")

file1.close()