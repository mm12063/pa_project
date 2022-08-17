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

PLOT_X_SIZE = 40
PLOT_Y_SIZE = 30
START_DATE = "01/01/2015"
END_DATE = "31/12/2015"

plt.style.use('seaborn')
plt.rcParams["figure.figsize"] = (PLOT_X_SIZE, PLOT_Y_SIZE)

mining_companies = [
    # 'CBAT_Bat',
    # 'ENS_Bat',
    # "TIA_Bat"
    # 'SQM_Min',
    # 'ALB_Min',
    # 'LAC_Min',
]

# company_type = "min"
company_type = "bat"
company_type_dir = "battery_manufacturers"
# company_type_dir = "mining"

export_as_csv = False
save_plots = False

for company in mining_companies:
    filename = f"{company}_{company_type}_stockdat"

    df = pd.read_csv(f"StockData/main_ds.csv", parse_dates=True)
    df = preprocessor.get_df_within_range(df, "Date", START_DATE, END_DATE)

    df.plot(x="Date", y=company, figsize=(PLOT_X_SIZE, PLOT_Y_SIZE), legend="Stationary", linewidth=1)


    # eval.print_adfuller_stats(df["Close"])

    # df["Close_Stationary"] = df["Close"].diff(periods=1)

    # Combining the 2 plots in one
    # combined_plot = df.plot(x="Date",
    #                         y="Close_Stationary",
    #                         figsize=(PLOT_X_SIZE, PLOT_Y_SIZE),
    #                         ax=p1,
    #                         title=company)
    #
    # if save_plots:
    #     fig = combined_plot.get_figure()
    #     fig.savefig(f"plots/{company}_{company_type}__non_to_stationary.png")
    #
    # eval.print_adfuller_stats(df["Close_Stationary"].dropna())
    #
    # if export_as_csv:
    #     df.to_csv(f"StockData/{company_type_dir}/stationary/{company}_{company_type}__stationary_close.csv")
