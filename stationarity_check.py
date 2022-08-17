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

dir = "mining"
companies = [
    "CBAT_bat",
    "ENS_bat",
    "Tianqi_bat",
    "ALB_Min",
    "LAC_Min",
    "SQM_Min",
]

# company_type = "min"
# company_type_dir = "mining"
company_type = "bat"


export_as_csv = False
save_plots = False

for company in companies:
    filename = f"{company}_stockdat"

    if (company.split("_")[1] == "bat"):
        company_type_dir = "battery_manufacturers"
    else:
        company_type_dir = "mining"

    df = pd.read_csv(f"StockData/{company_type_dir}/{filename}.csv", parse_dates=True)
    df = preprocessor.get_df_within_range(df, "Date", START_DATE, END_DATE)

    print(f"{company} Stationary Check")
    eval.print_adfuller_stats(df["Close"])


print("========= Make non-stationary =========\n")

for company in companies:
    filename = f"{company}_stockdat"

    if (company.split("_")[1] == "bat"):
        company_type_dir = "battery_manufacturers"
    else:
        company_type_dir = "mining"

    df = pd.read_csv(f"StockData/{company_type_dir}/{filename}.csv", parse_dates=True)
    df = preprocessor.get_df_within_range(df, "Date", START_DATE, END_DATE)

    print(f"{company} Stationary Check")

    df["Close_Stationary"] = df["Close"].diff(periods=1)

    eval.print_adfuller_stats(df["Close_Stationary"].dropna())



