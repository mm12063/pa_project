import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('StockData/main_ds.csv')
# df = df.set_index("Date")
df.columns.name = "company"
print(df.head())

y_cols = [
    'ENS_Bat',
    'TIA_Bat',
    'ALB_Min',
    'LAC_Min',
    'CBAT_Bat',
    'SQM_Min'
]

# df = px.data.stocks(indexed=True)-1
# print(df.head())

# fig = px.area(df, facet_col="company", facet_col_wrap=3)
# fig.update_traces(line=dict(width=1))
# fig.show()

fig = px.line(df, x="Date", y=df.columns,
              title='')
fig.update_traces(line=dict(width=1))
# fig.update_xaxes(
    # dtick="M1",
    # tickformat="%b\n%Y",
    # ticklabelmode="period")
fig.show()


#
# fig = go.Figure([go.Scatter(df, x='Date', y=y_cols)])
# fig.show()

#
# fig = px.line(df, x='Date', y=y_cols)
#
# fig.update_layout(
#     title="All Mining and Battery Closing Prices",
#     xaxis_title="Date",
#     yaxis_title="Closing",
#     legend_title="Battery and Mining Companies"
# )
#
# fig.update_xaxes(
#     rangeslider_visible=True,
#     rangeselector=dict(
#         buttons=list([
#             dict(step="all")
#         ])
#     )
# )
#
#

# fig.show()
