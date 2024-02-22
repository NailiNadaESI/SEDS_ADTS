import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from matplotlib.cbook import boxplot_stats

import streamlit as st

st.set_page_config(page_title='Modeling ', page_icon='💻')
st.markdown('# 💻 Modeling :')

st.write ("### The pretraited training dataset:")

train_hours = 80*7*24
test_hours = 15*7*24 
trained = pd.read_csv('data/FixedTrain.csv')
train = pd.read_csv('data/train.csv')
df_day=pd.read_csv('data/PreprocessedData.csv')

trained.rename(columns={"Unnamed: 0":"Date"},inplace=True)
trained['Date'] = pd.to_datetime(trained['Date'])
trained.set_index("Date", inplace=True)

train.rename(columns={"Unnamed: 0":"Date"},inplace=True)
train['Date'] = pd.to_datetime(train['Date'])
train.set_index("Date", inplace=True)

df_day.rename(columns={"Unnamed: 0":"Date"},inplace=True)
df_day['Date'] = pd.to_datetime(df_day['Date'])
df_day.set_index("Date", inplace=True)
st.write(df_day)

month_mean_train = train.groupby(train.index.month).mean()

train_uni = trained['Total'].copy()
test_uni = df_day['Total'][(train_hours//24):].copy()
test_uni = test_uni - test_uni.index.month.map(month_mean_train['Total'])

train.drop('Total', inplace=True, axis=1)


st.write ("##  Univariante Anomaly detection :")
st.write ("In this project I chose to go with studing the anomalies based on one variable that is the total using the ARIMA algorithm")
st.write (" First we'll try find the best model based on the best AIC and the best Order")
st.write("- **Order(p,d,q)** : it's a set of parameters defining the structure of a model  : ")
st.write ("p (Autoregression Order) : represents the number of past time points used to predict the current value , the higher the better ." )
st.write ("d (Differencing Order) : represents the numberof times the raw observations are differenced to make the time series stationary, it only takes 0 or 1")
st.write ("q (Moving average Order) : indecates the number of past forecast errors used to predict the current value")

st.write("- **AIC(Akaike Information Criterion)** : The AIC is a measure of the model's goodness of fit, taking into account the complexity of the model. the lower the AIC the better")

AIC = {}
best_aic, best_order = np.inf, 0

for p in range(6, 9):
    for q in range(0, 10):
        mod = SARIMAX(train_uni, order=(p, 0, q), enforce_invertibility=False)
        try:
            res = mod.fit(disp=False)
            AIC[(p, 0, q)] = res.aic
        except:
            AIC[(p, 0, q)] = np.inf

        if AIC[(p, 0, q)] < best_aic:
            best_aic = AIC[(p, 0, q)]
            best_order = (p, 0, q)

with open('aic_results.txt', 'w') as file:
    for order, aic in AIC.items():
        file.write(f"{order}: {aic}\n")
            
st.write("After applying the algorithm one the dataset we found that : ")
st.write('BEST ORDER : ',best_order)
st.write('BEST AIC:', best_aic)


st.write("Now we have to train the best univariante model and visualize it's performance ")
mod = SARIMAX(train_uni, order=best_order, enforce_invertibility=False)
res = mod.fit(disp=False)

st.pyplot(res.plot_diagnostics(figsize=(18,10)))

st.write("### Get and fit train fitted values :")
st.write(" In the following section we will be making a prediction on the training set to define the confidence interval as well as the predected values ")
predict = res.get_prediction()
predicted_mean = predict.predicted_mean + predict.predicted_mean.index.month.map(month_mean_train['Total'])
train_uni = train_uni + train_uni.index.month.map(month_mean_train['Total'])
predict_ci = predict.conf_int(alpha=0.1)
predict_ci['lower Total'] = predict_ci.apply(lambda x: x['lower Total'] + month_mean_train['Total'][x.name.month], axis=1)
predict_ci['upper Total'] = predict_ci.apply(lambda x: x['upper Total'] + month_mean_train['Total'][x.name.month], axis=1)

residuals_mean = res.resid.mean()
residuals_std = res.resid.std()

fig, ax = plt.subplots(figsize=(15, 6))

ax.plot(train_uni, 'k.', label='Actual Data')
ax.plot(predicted_mean, linestyle='--', linewidth=2, color='blue', label='Predicted')
ax.fill_between(predict_ci.index, predict_ci['lower Total'], predict_ci['upper Total'], alpha=0.6, label='Confidence Interval')

ax.set_xlabel('Date')
ax.legend()

st.pyplot(fig)
st.write("### Iterative prediction on test data")
st.write(" Same as the trainin set we'll make some predictions on the values of the test set ")
point_forecast = res.get_prediction(end=mod.nobs)
point_ci = point_forecast.conf_int(alpha=0.1)
print (point_ci)
mean_pred = {point_forecast.predicted_mean.index[-1]: point_forecast.predicted_mean[-1]}
upper_pred = {point_ci.index[-1]: point_ci['upper Total'][-1]}
lower_pred = {point_ci.index[-1]: point_ci['lower Total'][-1]}

print(mean_pred)
for t,row in test_uni[:-1].items():
    
    row = pd.Series(row, index=[t])
    res = res.extend(row)
    point_forecast = res.get_prediction(1)
    point_ci = point_forecast.conf_int(alpha=0.1)
    
    mean_pred[point_forecast.predicted_mean.index[0]] = point_forecast.predicted_mean.values[0]
    upper_pred[point_ci.index[0]] = point_ci['upper Total'][0]
    lower_pred[point_ci.index[0]] = point_ci['lower Total'][0]
    
mean_pred = pd.Series(mean_pred)
upper_pred = pd.Series(upper_pred)
lower_pred = pd.Series(lower_pred)



alpha = 0.01
upper = stats.norm.ppf(1 - alpha/2)
lower = stats.norm.ppf(alpha/2)

residuals_test = test_uni - residuals_mean
residuals_test = (residuals_test - residuals_mean) / residuals_std

fig, ax = plt.subplots(figsize=(15, 6))
ax.plot(residuals_test)
ax.set_ylabel('resid')
ax.axhline(upper, c='red', linestyle='--')
ax.axhline(lower, c='red', linestyle='--')

st.pyplot(fig)


st.write("### REVERSE SCALING TEST ITERATIVE PREDICTIONS ")
mean_pred = mean_pred + mean_pred.index.month.map(month_mean_train['Total'])
upper_pred = upper_pred + upper_pred.index.month.map(month_mean_train['Total'])
lower_pred = lower_pred + lower_pred.index.month.map(month_mean_train['Total'])
test_uni = test_uni + test_uni.index.month.map(month_mean_train['Total'])

plt.figure(figsize=(15, 6))
plt.plot(test_uni, 'k.')


plt.plot(mean_pred, linestyle='--', linewidth=2, color='blue')
plt.fill_between(mean_pred.index, lower_pred, upper_pred, alpha=0.6)


outside_borders = (test_uni < lower_pred) | (test_uni > upper_pred)


plt.plot(test_uni[outside_borders].index, test_uni[outside_borders], 'ro', markersize=8)


st.pyplot(plt)