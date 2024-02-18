import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

import streamlit as st

st.set_page_config(page_title='Modeling ', page_icon='💻')
st.markdown('# 💻 Modeling :')

st.write ("### The training dataset:")
train = pd.read_csv('data/PreprocessedData_Train.csv')
train.rename(columns={"Unnamed: 0":"Date"},inplace=True)
train['Date'] = pd.to_datetime(train['Date'])
train.set_index("Date", inplace=True)
st.write(train)

st.write ("## 1/ Univariante Anomaly detection :")
st.write ("In this project I chose to go with studing the anomalies based on one variable that is the total using the ARIMA algorithm")
st.write (" First we'll try find the best model based on the best AIC and the best Order")
st.write("- **Order(p,d,q)** : it's a set of parameters defining the structure of a model  : ")
st.write ("p (Autoregression Order) : represents the number of past time points used to predict the current value , the higher the better ." )
st.write ("d (Differencing Order) : represents the numberof times the raw observations are differenced to make the time series stationary, it only takes 0 or 1")
st.write ("q (Moving average Order) : indecates the number of past forecast errors used to predict the current value")

st.write("- **AIC(Akaike Information Criterion)** : The AIC is a measure of the model's goodness of fit, taking into account the complexity of the model. the lower the AIC the better")

def Arima():
    AIC = {}
    best_aic, best_order = np.inf, 0

    for p in range(6, 9):
        for q in range(0, 10):
            mod = SARIMAX(train['Total'], order=(p, 0, q), enforce_invertibility=False)
            try:
                res = mod.fit(disp=False)
                AIC[(p, 0, q)] = res.aic
            except:
                AIC[(p, 0, q)] = np.inf
            if AIC[(p, 0, q)] < best_aic:
                best_aic = AIC[(p, 0, q)]
                best_order = (p, 0, q)

    with open('Arima.txt', 'w') as file:
        file.write(str(best_order) + '\n')
        file.write(str(best_aic))
    return best_order, best_aic
def read_Arima_results():
    try:
        with open('Arima.txt', 'r') as file:
            lines = file.readlines()
            best_order = tuple(map(int, lines[0].strip()[1:-1].split(',')))
            best_aic = float(lines[1].strip())

            return best_order, best_aic

    except FileNotFoundError:
        Arima()

best_order, best_aic = read_Arima_results()

st.write("After applying the algorithm one the dataset we found that : ")
st.write('BEST ORDER : '+str(best_order))
st.write('BEST AIC:', str(best_aic))

st.write("Now we have to train the best univariante model and visualize it's performance ")
mod = SARIMAX(train['Total'], order=best_order, enforce_invertibility=False)
res = mod.fit(disp=False)

st.pyplot(res.plot_diagnostics(figsize=(18,10)))
 

st.write("#### train and plot fitted values : ")
trained = pd.read_csv('data/train.csv')

trained.rename(columns={"Unnamed: 0": "Date"}, inplace=True)
trained['Date'] = pd.to_datetime(trained['Date'])

trained.set_index("Date", inplace=True)
month_mean_train = trained.groupby(trained.index.month).mean()
predict = res.get_prediction()
predicted_mean = predict.predicted_mean + predict.predicted_mean.index.month.map(month_mean_train['Total'])
train_uni = train['Total'] + train.index.month.map(month_mean_train['Total'])
predict_ci = predict.conf_int(alpha=0.1)
predict_ci['lower Total'] = predict_ci.apply(lambda x: x['lower Total'] + month_mean_train['Total'][x.name.month], axis=1)
predict_ci['upper Total'] = predict_ci.apply(lambda x: x['upper Total'] + month_mean_train['Total'][x.name.month], axis=1)

residuals_mean = res.resid.mean()
residuals_std = res.resid.std()

fig, ax = plt.subplots(figsize=(15, 6))

ax.plot(train_uni, 'k.', label='Actual Data')
ax.plot(predicted_mean, linestyle='--', linewidth=2, color='blue', label='Predicted Mean')
ax.fill_between(predict_ci.index, predict_ci['lower Total'], predict_ci['upper Total'], alpha=0.6, label='Confidence Interval')

ax.set_xlabel('Date')
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)