import pandas as pd 
import numpy as np 
import streamlit as st

st.set_page_config(page_title='Preprocessing ', page_icon='🗒️')
st.markdown('# 🗒️ Preprocessing :')

def preprocess_app():
    

    st.write ("### 1/ Loading the dataset:")
    train_hours = 100*7*24 
    test_hours = 20*7*24  

    df = pd.read_csv('data/bike-and-ped-counter.csv.zip', nrows=train_hours+test_hours, parse_dates=['Date'])


    #df.set_index('Date')
    st.write(df)

    st.write("First we need to have a global idea about the dataset by generating  a small description of the dataset")
    st.table(df.describe())

    st.write ("### 2/ Handeling Missing values:")
    st.write("#### Identifying Null values:")
    st.write('We need to identify the null values in the dataset')
    st.table(df.isna().sum())
    st.write("We have found 5 missing values in the dataset")

    st.write("#### Handeling Null values:")
    df['Ped South'] = df['Ped South'].groupby(df.Date.dt.hour).transform(lambda x: x.fillna(x.mean()))
    df['Ped North'] = df['Ped North'].groupby(df.Date.dt.hour).transform(lambda x: x.fillna(x.mean()))
    df['Bike South'] = df['Bike South'].groupby(df.Date.dt.hour).transform(lambda x: x.fillna(x.mean()))
    df['Bike North'] = df['Bike North'].groupby(df.Date.dt.hour).transform(lambda x: x.fillna(x.mean()))
    df['BGT North of NE 70th Total'] = df['Ped South'] + df['Ped North'] + df['Bike South'] + df['Bike North']

    df['Date'] = pd.to_datetime(df['Date'].dt.date)
    st.write("In order to get rid of the missing values , it's enough to replace them using the mean value :")
    st.table(df.isna().sum())
    st.table(df.describe())

    st.write("### 3/ Aggregation :")
    st.write("Next step is to aggregate the data that we have , so instead of having the data by hour we'll  have them by day while making the day the new index of the dataset")
    df_day = pd.DataFrame()
    df_day['Ped South'] = df.groupby(df.Date)['Ped South'].sum()
    df_day['Ped North'] = df.groupby(df.Date)['Ped North'].sum()
    df_day['Bike South'] = df.groupby(df.Date)['Bike South'].sum()
    df_day['Bike North'] = df.groupby(df.Date)['Bike North'].sum()
    df_day['Total'] = df.groupby(df.Date)['BGT North of NE 70th Total'].sum()

    df_day.index = pd.DatetimeIndex(df_day.index.values, freq=df_day.index.inferred_freq)
    df_day.to_csv("data/preprocessedData.csv")
    st.write(df_day)

preprocess_app()