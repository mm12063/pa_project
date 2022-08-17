import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf, month_plot, quarter_plot

companies = [
    "CBAT_Bat",
    "ENS_Bat",
    "TIA_Bat",
    "ALB_Min",
    "LAC_Min",
    "SQM_Min",
]

export_plot = False

for company in companies:

    df = pd.read_csv(f"StockData/main_ds.csv", parse_dates=True)

    fig, ax = plt.subplots(2)
    plot_acf(df[company], ax=ax[0])
    plot_pacf(df[company], ax=ax[1])
    fig.set_size_inches((16, 9))
    fig.suptitle(f"{company} ACF and PACF Plots", fontsize=16)
    plt.show()

    if export_plot:
        fig.savefig(f"plots/auto_correlation/{company}__acf_pacf_plots")


