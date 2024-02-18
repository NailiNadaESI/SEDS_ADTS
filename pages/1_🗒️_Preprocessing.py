import streamlit as st

import numpy as np
import pandas as pd
import os 
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.vector_ar.var_model import VAR


st.set_page_config(page_title='Preprocessing ', page_icon='🗒️')
st.markdown('# 🗒️ Preprocessing :')

st.write("### 1/ Loading the dataset:")
train_hours = 80*7*24
test_hours = 15*7*24  

df = pd.read_csv('data/bike-and-ped-counter.csv.zip', nrows=train_hours+test_hours, parse_dates=['Date'])
st.write(df)

st.write("First we need to have a global idea about the dataset by generating a small description of the dataset")
st.table(df.describe())

st.write("### 2/ Handeling Missing values:")
st.write("#### Identifying Null values:")
st.write('We need to identify the null values in the dataset')
st.table(df.isna().sum())
st.write("We have found 4 missing values in the dataset")

st.write("#### Handeling Null values:")
df['Ped South'] = df['Ped South'].groupby(df.Date.dt.hour).transform(lambda x: x.fillna(x.mean()))
df['Ped North'] = df['Ped North'].groupby(df.Date.dt.hour).transform(lambda x: x.fillna(x.mean()))
df['Bike South'] = df['Bike South'].groupby(df.Date.dt.hour).transform(lambda x: x.fillna(x.mean()))
df['Bike North'] = df['Bike North'].groupby(df.Date.dt.hour).transform(lambda x: x.fillna(x.mean()))
df['BGT North of NE 70th Total'] = df['Ped South'] + df['Ped North'] + df['Bike South'] + df['Bike North']

df['Date'] = pd.to_datetime(df['Date'].dt.date)
st.write("In order to get rid of the missing values, it's enough to replace them using the mean value:")
st.table(df.isna().sum())
st.table(df.describe())

st.write("### 3/ Aggregation:")
st.write("Next step is to aggregate the data that we have, so instead of having the data by hour, we'll have them by day while making the day the new index of the dataset")
df_day = pd.DataFrame()
df_day['Ped South'] = df.groupby(df.Date)['Ped South'].sum()
df_day['Ped North'] = df.groupby(df.Date)['Ped North'].sum()
df_day['Bike South'] = df.groupby(df.Date)['Bike South'].sum()
df_day['Bike North'] = df.groupby(df.Date)['Bike North'].sum()
df_day['Total'] = df.groupby(df.Date)['BGT North of NE 70th Total'].sum()

df_day.index = pd.DatetimeIndex(df_day.index.values, freq=df_day.index.inferred_freq)
st.write(df_day)

st.write("### 4/ Plotting The data:")
columns = df_day.columns.difference(['Date'])
colors = ['orange', 'green', 'red', 'purple', 'blue']

fig, axes = plt.subplots(nrows=len(columns), ncols=1, figsize=(16, 6 * len(columns)))

for clm, color, ax in zip(columns, colors, axes):
  df_day[clm].plot(ax=ax, color=color)
  ax.set_xlabel('Date')
  ax.set_ylabel('Values')
  ax.set_title(f'Plot of {clm}')

plt.tight_layout()
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(16, 6))
for clm, color in zip(columns, colors):
   df_day[clm].plot(ax=ax, color=color, label=clm)
ax.set_xlabel('Date')
ax.set_ylabel('Values')
ax.set_title('Plot of All Columns')
ax.legend()
st.pyplot(fig)

train = df_day[:(train_hours//24)].copy()
train.to_csv('data/train.csv')
st.write(" ###### Plotting the autocorrelation:")

fig, ax = plt.subplots(figsize=(16, 6))
pd.plotting.autocorrelation_plot(df_day.iloc[:train_hours]['Total'], ax=ax)
ax.set_title("Autocorrelation Plot")
st.pyplot(fig)

st.write("We need to remove the long term seasonality")

month_mean_train = train.groupby(train.index.month).mean()
train['Ped South'] = train.apply(lambda x: x['Ped South'] - month_mean_train['Ped South'][x.name.month], axis=1)
train['Ped North'] = train.apply(lambda x: x['Ped North'] - month_mean_train['Ped North'][x.name.month], axis=1)
train['Bike South'] = train.apply(lambda x: x['Bike South'] - month_mean_train['Bike South'][x.name.month], axis=1)
train['Bike North'] = train.apply(lambda x: x['Bike North'] - month_mean_train['Bike North'][x.name.month], axis=1)
train['Total'] = train.apply(lambda x: x['Total'] - month_mean_train['Total'][x.name.month], axis=1)

fig, ax = plt.subplots(figsize=(16, 6))
pd.plotting.autocorrelation_plot(train['Total'],ax=ax)
ax.set_title("Autocorrelation Plot")
st.pyplot(fig)

if not os.path.exists('data/PreprocessedData_Train.csv'):
  train.to_csv('data/PreprocessedData_Train.csv')
if not os.path.exists('data/PreprocessedData_Test.csv'):
   df_day[(test_hours//24):].to_csv('data/PreprocessedData_Test.csv')
