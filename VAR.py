from statsmodels.tsa.api import VAR
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.stats.stattools import durbin_watson

plt.style.use('seaborn')
plt.rcParams["figure.figsize"] = (40, 30)

df = pd.read_csv(f"StockData/main_ds.csv", parse_dates=True)

df = df.set_index("Date")

num_to_predict = 3
train_df, test_df = df[0:-num_to_predict], df[-num_to_predict:]

train_df = train_df[
    [
    'CBAT_Bat',
    'ENS_Bat',
    'TIA_Bat',
    'ALB_Min',
    'LAC_Min',
    'SQM_Min',
]]


model = VAR(train_df)

#TODO SHOW IN SLIDES

# Find best lag order (min before it's starts to increase again – overfitting)
for i in range(1,20):
    result = model.fit(i)
    print(f'Lag: {i}')
    print(f'AIC: {result.aic} \n')

best_lag = 2  # 2 was the best AIC

model_fitted = model.fit(maxlags=best_lag)
print(model_fitted.summary())



#TODO SHOW IN SLIDES

# Check if there is any correlation in the residuals [0-4]. 
# 2 = No signif serial correlation
# 0 = positive serial correlation
# 4 = negative serial correlation
resids = durbin_watson(model_fitted.resid)
for col, val in zip(df.columns, resids):
    print(f"{col}: {round(val,2)}")





test_df = test_df.loc[:, ~test_df.columns.str.contains('^Unnamed')]
lag_order = model_fitted.k_ar



forecast_input = train_df.values[-lag_order:]
print(forecast_input)


fc = model_fitted.forecast(y=forecast_input, steps=num_to_predict)
print(fc)


smaller_df = df.loc[:, ~df.columns.isin(['Month', 'Year'])]
smaller_df = smaller_df.loc[:, ~smaller_df.columns.str.contains('^Unnamed')]

pred_df = pd.DataFrame(fc, index=smaller_df.index[-num_to_predict:], columns=smaller_df.columns + '_pred')
print(pred_df)




# SHOW IN SLIDES
fig, axes = plt.subplots(nrows=int(len(smaller_df.columns)/2), ncols=2, dpi=150, figsize=(10,10))
for i, (col,ax) in enumerate(zip(smaller_df.columns, axes.flatten())):
    pred_df[col+'_pred'].plot(legend=True, ax=ax).autoscale(axis='x',tight=True)
    test_df[col][-num_to_predict:].plot(legend=True, ax=ax)
    ax.set_title(col + ": Predicted vs Actuals")
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.spines["top"].set_alpha(0)
    ax.tick_params(labelsize=6)

plt.tight_layout()





#TODO SHOW IN SLIDES – How to interpret???

def get_accuracy(predicted, actual):
    mape = np.mean(np.abs(predicted - actual)/np.abs(actual))
    rmse = np.mean((predicted - actual)**2)**.5
    return({
        'MAPE': mape,
        'RMSE': rmse
    })


for col in smaller_df.columns:
    print(f"Accuracy of: {col}")
    accuracy_prod = get_accuracy(pred_df[f"{col}_pred"].values, test_df[col])
    for key, val in accuracy_prod.items():
        print(f"{key}: {round(val, 4)}")
    print("")






#TODO SHOW IN SLIDES – how to interpret?

# Impulse response
irf = model_fitted.irf(num_to_predict)
irf.plot(figsize=(20, 20))
plt.rcParams["figure.figsize"] = (40, 30)

plt.show()





