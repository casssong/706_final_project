import altair as alt
import pandas as pd
import streamlit as st

@st.cache

#load data
#add country-codes
covid_df = pd.read_csv('processed_data.csv')
country_df = pd.read_csv('https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/country_codes.csv', dtype = {'conuntry-code': str})
covid_df=covid_df.rename(columns = {'location':'Country'})
covid_df = covid_df.merge(country_df[['Country','country-code']],how='left', on=['Country'])

st.write("## COVID-19 cases from 2021 to 2022")

#bar plot global: 


#pie chart multiple countries:


#map specific countries:

#line plot:

#bar plot: