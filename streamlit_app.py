import altair as alt
import pandas as pd
import streamlit as st

covid_df = pd.read_csv('processed_data.csv')

st.write("## COVID-19 cases from 2021 to 2022")

