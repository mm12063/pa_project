import pandas as pd
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf, month_plot, quarter_plot

from Data_Evaluator import Data_Evaluator
from Data_Preprocessor import Data_Preprocessor

preprocessor = Data_Preprocessor()

dir = "mining"
companies = [
    # "CBAT_bat",
    # "ENS_bat",
    # "Tianqi_002466_SZ_bat",
    "ALB_Min",
    # "LAC_Min",
    # "SQM_Min",
]

display_plots = True
polar_plots = False
line_plots = False
save_dcomp_plots = True
decom_plots = True


for company in companies:
    dcomp_year = 2015

    df = pd.read_csv(f"StockData/{dir}/stationary/{company}__stationary_close.csv", parse_dates=True)

    # Add month and year columns to main df
    months = []
    years = []
    date_format = '%Y %m %d'
    splitter = '-'
    for index, row in df.iterrows():
        date = row["Date"]
        month = datetime.datetime.strptime(date.replace(splitter, " "), date_format).strftime("%b")
        year = datetime.datetime.strptime(date.replace(splitter, " "), date_format).year
        months.append(month)
        years.append(year)

    df["Month"] = months
    df["Year"] = years


    if display_plots:
        if polar_plots:
            fig = px.line_polar(df, r='Close_USD', theta='Month',
                                color='Year', line_close=True,
                                title=f"{company} Polar Seasonal Plot",
                                width=600, height=500)
            fig.show()

        if line_plots:
            plot = sns.lineplot(data=df,
                         x='Month',
                         y='Close',
                         hue='Year',
                         legend='full',
                         ci=None)

            fig = plot.get_figure()
            fig.savefig(f"plots/{company}__seasonality_polar")

            plt.show()

        if decom_plots:
            for i in range(0,5):
                print(dcomp_year)
                START_DATE = f"{dcomp_year}-01-01"
                END_DATE = f"{dcomp_year}-12-31"
                df_range = preprocessor.get_df_within_range(df, "Date", START_DATE, END_DATE)

                decomposition = seasonal_decompose(df_range['Close'],
                                                   model='multiplicative',
                                                   period=12)

                fig = decomposition.plot()
                fig.set_size_inches((16, 9))
                fig.suptitle(f"{company} {dcomp_year} DComp Plot", fontsize=16)
                plt.show()

                if save_dcomp_plots:
                    fig.savefig(f"plots/dcomp/{company}__{dcomp_year}_dcomp_plot.png")
                dcomp_year = dcomp_year+1
