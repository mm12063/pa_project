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
from plotly.subplots import make_subplots
import statsmodels.api as sm
pd.options.mode.chained_assignment = None  # default='warn'

startdate = pd.to_datetime('2014-11-13')
enddate = pd.to_datetime('2015-6-30')
stock='ALB'


print(" [The current Stock : "+stock+" ] ")
df = data.DataReader(stock, 'yahoo', startdate, enddate)
print(df.head(30))
df.ta.macd(close='Adj Close', fast=12, slow=26, signal=9, append=True)
print(df.head(30))
print(" [ After Reindexing ]")
df = df.iloc[33:]

ndf = df[['Adj Close','MACD_12_26_9','MACDh_12_26_9','MACDs_12_26_9']]
print(ndf)


df.columns = [x.lower() for x in df.columns]

fig = make_subplots(rows=2, cols=1)
# price Line
fig.append_trace(
    go.Scatter(
        x=df.index,
        y=df['open'],
        line=dict(color='#ff9900', width=1),
        name='open',
        # showlegend=False,
        legendgroup='1',
    ), row=1, col=1
)
# Candlestick chart for pricing
fig.append_trace(
    go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        increasing_line_color='#ff9900',
        decreasing_line_color='black',
        showlegend=False
    ), row=1, col=1
)
# Fast Signal (%k)
fig.append_trace(
    go.Scatter(
        x=df.index,
        y=df['macd_12_26_9'],
        line=dict(color='#ff9900', width=2),
        name='macd',
        # showlegend=False,
        legendgroup='2',
    ), row=2, col=1
)
# Slow signal (%d)
fig.append_trace(
    go.Scatter(
        x=df.index,
        y=df['macds_12_26_9'],
        line=dict(color='#000000', width=2),
        # showlegend=False,
        legendgroup='2',
        name='signal'
    ), row=2, col=1
)
# Colorize the histogram values
colors = np.where(df['macdh_12_26_9'] < 0, '#000', '#ff9900')
# Plot the histogram
fig.append_trace(
    go.Bar(
        x=df.index,
        y=df['macdh_12_26_9'],
        name='histogram',
        marker_color=colors,
    ), row=2, col=1
)
# Make it pretty
layout = go.Layout(
    plot_bgcolor='#efefef',
    # Font Families
    font_family='Monospace',
    font_color='#000000',
    font_size=20,
    xaxis=dict(
        rangeslider=dict(
            visible=False
        )
    )
)
# Update options and show plot
fig.update_layout(layout)
fig.show()

