import streamlit as st

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.vector_ar.var_model import VAR

st.set_page_config(page_title='Visualization ', page_icon='📊')
st.markdown('# 📊 Visualization :')

st.write("### 1/The preprocessed dataset:")
df = pd.read_csv('data/preprocessedData.csv')
df = df.rename(columns={"Unnamed: 0": "Date"})
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
st.write(df)

st.write("### 2/Plotting The data:")
columns = df.columns.difference(['Date'])
colors = ['blue', 'green', 'red', 'purple', 'orange']

fig, axes = plt.subplots(nrows=len(columns), ncols=1, figsize=(16, 6 * len(columns)))

for clm, color, ax in zip(columns, colors, axes):
    df[clm].plot(ax=ax, color=color)
    ax.set_xlabel('Date')
    ax.set_ylabel('Values')
    ax.set_title(f'Plot of {clm}')
    
plt.tight_layout()
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(16, 6))
for clm, color in zip(columns, colors):
    df[clm].plot(ax=ax, color=color, label=clm)
ax.set_xlabel('Date')
ax.set_ylabel('Values')
ax.set_title('Plot of All Columns')
ax.legend()
st.pyplot(fig)
