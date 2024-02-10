import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.vector_ar.var_model import VAR

import streamlit as st

st.set_page_config(page_title='Modeling ', page_icon='💻')
st.markdown('# 💻 Modeling :')

st.write ("### 1/ The dataset:")