import altair as alt
import pandas as pd
import streamlit as st

@st.cache

#load data
covid_df = pd.read_csv('processed_data.csv')
#add country-codes
country_df = pd.read_csv('https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/country_codes.csv', dtype = {'conuntry-code': str})
covid_df = covid_df.rename(columns = {'location':'Country'})
covid_df = covid_df.merge(country_df[['Country','country-code']],how='left', on=['Country'])

#world data
data_world = data[data['Country']=='World']

#country data
country_drop =  ['Africa', 'Asia', 'Europe', 'European Union', 'High income', 'International', 'Low income', 'Lower middle income', 'North America', 'Oceania', 'South America', 'Upper middle income', 'World']
data_country = data.copy()
data_country = data_country[~pd.DataFrame(data_country.Country.tolist()).isin(country_drop).any(1).values]

st.write("## COVID-19 cases of 2021")

#line plot global: 

#selector month:

#map specific countries:

#
#bar plot: