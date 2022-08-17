import pandas as pd
import matplotlib.pyplot as plt
import datetime

export_as_csv = False


# Stock data
cbat_df = pd.read_csv(f"StockData/battery_manufacturers/stationary/CBAT_bat__stationary_close.csv", parse_dates=True)
ens_df = pd.read_csv(f"StockData/battery_manufacturers/stationary/ENS_bat__stationary_close.csv", parse_dates=True)
tianqi_df = pd.read_csv(f"StockData/battery_manufacturers/stationary/Tianqi_002466_SZ_bat__stationary_close.csv", parse_dates=True)

alb_df = pd.read_csv(f"StockData/mining/stationary/ALB_min__stationary_close.csv", parse_dates=True)
lac_df = pd.read_csv(f"StockData/mining/stationary/LAC_min__stationary_close.csv", parse_dates=True)
sqm_df = pd.read_csv(f"StockData/mining/stationary/SQM_min__stationary_close.csv", parse_dates=True)

lithium_news_df = pd.read_csv(f"data/csv/compiled/sentimentally/lithium.csv", parse_dates=True)
alb_news_df = pd.read_csv(f"data/csv/compiled/sentimentally/albemarle.csv", parse_dates=True)
sqm_news_df = pd.read_csv(f"data/csv/compiled/sentimentally/sqm.csv", parse_dates=True)



main_df = pd.DataFrame()

main_df["Date"] = cbat_df["Date"]
main_df["CBAT_Bat"] = cbat_df["Close_Stationary"]
# main_df = main_df.set_index("Date")
print(main_df.head())

ds_len = len(main_df.index)

main_df["ENS_Bat"] = [0.0] * ds_len
cond = main_df['Date'] == ens_df["Date"]
main_df.loc[cond,'ENS_Bat'] = ens_df["Close_Stationary"]


temp = []
for index, row in main_df.iterrows():
    selected_row = tianqi_df.loc[tianqi_df["Date"] == row["Date"]]

    if len(selected_row):
        temp.append(float(selected_row["Close_Stationary"]))
    else:
        temp.append(0.0)

print(len(temp))
main_df["TIA_Bat"] = temp



main_df["ALB_Min"] = [0.0] * ds_len
cond = main_df['Date'] == alb_df["Date"]
main_df.loc[cond,'ALB_Min'] = alb_df["Close_Stationary"]

main_df["LAC_Min"] = [0.0] * ds_len
cond = main_df['Date'] == lac_df["Date"]
main_df.loc[cond,'LAC_Min'] = lac_df["Close_Stationary"]

main_df["SQM_Min"] = [0.0] * ds_len
cond = main_df['Date'] == sqm_df["Date"]
main_df.loc[cond,'SQM_Min'] = sqm_df["Close_Stationary"]


# main_df["CBAT_Bat"] = cbat_df["Close_Stationary"]
# main_df["ENS_Bat"] = ens_df["Close_Stationary"]
# main_df["TIA_Bat"] = tianqi_df["Close_Stationary"]
#
# main_df["ALB_Min"] = alb_df["Close_Stationary"]
# main_df["LAC_Min"] = lac_df["Close_Stationary"]
# main_df["SQM_Min"] = sqm_df["Close_Stationary"]

print(main_df.head())
# print(main_df.tail())


# for index, row in main_df.iterrows():
#     selected_row = ens_df.loc[ens_df["Date"] == row["Date"]]
#     if len(selected_row):
#         # print(main_df.loc[row["Date"]])
#         row["ENS_Bat"] = selected_row["Close_Stationary"]
#         row["ENS_Bat"] = 2.0



# main_df["CBAT_Bat"] = cbat_df["Close_Stationary"]
# main_df["ENS_Bat"] = ens_df["Close_Stationary"]
# main_df["TIA_Bat"] = tianqi_df["Close_Stationary"]
#
# main_df["ALB_Min"] = alb_df["Close_Stationary"]
# main_df["LAC_Min"] = lac_df["Close_Stationary"]
# main_df["SQM_Min"] = sqm_df["Close_Stationary"]




# main_df["News_Lithium_NLTK"] = lithium_news_df["snippet_sentiment"]
# main_df["News_ALB_NLTK"] = alb_news_df["snippet_sentiment"]
# main_df["News_SQM_NLTK"] = sqm_news_df["snippet_sentiment"]

# lithium_news_df["date"]
# lithium_news_df["snippet_sentiment"]


# Reformat the date
new_dates = []
for index, row in main_df.iterrows():
    date = row["Date"]
    new_date = datetime.datetime.strptime(date.replace("-", " "), '%Y %m %d').strftime('%d/%m/%Y')
    new_dates.append(new_date)

main_df["Date"] = new_dates


# Add month and year columns to main df
months = []
years = []
for index, row in main_df.iterrows():
    date = row["Date"]
    month = datetime.datetime.strptime(date.replace("/", " "), '%d %m %Y').strftime("%b")
    year = datetime.datetime.strptime(date.replace("/", " "), '%d %m %Y').year
    months.append(month)
    years.append(year)

main_df["Month"] = months
main_df["Year"] = years


#
#
# for index, row in main_df.iterrows():
#     selected_row = lithium_news_df.loc[lithium_news_df['date'] == row["Date"]]
#
#     if len(selected_row) > 0:
#         print(selected_row["date"] +" "+ selected_row["source"])






# for index, row in lithium_news_df.iterrows():
#     print(row["date"])





# print(main_df.head())
print(main_df.tail())

if export_as_csv:
    main_df.to_csv(f"StockData/main_ds.csv")


