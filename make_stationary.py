import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from datetime import datetime
import seaborn as sns

# stats
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf, month_plot, quarter_plot
from statsmodels.tsa.stattools import adfuller

from Data_Evaluator import Data_Evaluator
from Data_Preprocessor import Data_Preprocessor

plt.interactive(True)  # Needed to make plots appear in PyCharm

preprocessor = Data_Preprocessor()
eval = Data_Evaluator()

# pd.options.plotting.backend = "plotly"

PLOT_X_SIZE = 20
PLOT_Y_SIZE = 10
START_DATE = "2015-01-01"
END_DATE = "2019-12-31"

plt.style.use('seaborn')
plt.rcParams["figure.figsize"] = (PLOT_X_SIZE, PLOT_Y_SIZE)

mining_companies = [
    # 'PCRFY',
    # 'ENS',
    "Tianqi_002466_SZ"
    # 'SQM',
    # 'ALB',
    # 'LAC',
]



# # Plot
# fig, axes = plt.subplots(nrows=4, ncols=2, dpi=120, figsize=(10,6))
# for i, ax in enumerate(axes.flatten()):
#     data = df[df.columns[i]]
#     ax.plot(data, color='red', linewidth=1)
#     # Decorations
#     ax.set_title(df.columns[i])
#     ax.xaxis.set_ticks_position('none')
#     ax.yaxis.set_ticks_position('none')
#     ax.spines["top"].set_alpha(0)
#     ax.tick_params(labelsize=6)
#
# plt.tight_layout()
# plt.show()




# company_type = "min"
company_type = "bat"
company_type_dir = "battery_manufacturers"
# company_type_dir = "mining"

export_as_csv = False
save_plots = False

for company in mining_companies:
    filename = f"{company}_{company_type}_stockdat"

    df = pd.read_csv(f"StockData/{company_type_dir}/{filename}.csv", parse_dates=True)
    df = preprocessor.get_df_within_range(df, "Date", START_DATE, END_DATE)

    # Convert CNY -> USD
    # df["Close_USD"] = df["Close"] * 0.1483

    p1 = df.plot(x="Date", y="Close_USD", figsize=(PLOT_X_SIZE, PLOT_Y_SIZE), legend="Non-stationary")

    eval.print_adfuller_stats(df["Close_USD"])

    df["Close_Stationary"] = df["Close_USD"].diff(periods=1)

    # Combining the 2 plots in one
    combined_plot = df.plot(x="Date",
                            y="Close_Stationary",
                            figsize=(PLOT_X_SIZE, PLOT_Y_SIZE),
                            ax=p1,
                            title=company)

    if save_plots:
        fig = combined_plot.get_figure()
        fig.savefig(f"plots/{company}_{company_type}__non_to_stationary.png")

    eval.print_adfuller_stats(df["Close_Stationary"].dropna())

    if export_as_csv:
        df.to_csv(f"StockData/{company_type_dir}/stationary/{company}_{company_type}__stationary_close.csv")
