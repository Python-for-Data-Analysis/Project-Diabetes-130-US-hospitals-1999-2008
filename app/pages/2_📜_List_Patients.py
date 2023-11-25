import streamlit as st
import time
import numpy as np
import pandas as pd

# Import our encoded dataframe
dataF=pd.read_csv('dataframe_encoded.csv')
st.set_page_config(page_title="List Patients", page_icon="🏥")

st.markdown("# List Patients")
st.sidebar.header("List Patients")
st.write(
    """Add df + visu"""
)