import altair as alt
import pandas as pd
import streamlit as st

alt.data_transformers.disable_max_rows()

#load data
covid_df = pd.read_csv('processed_data.csv')
#add country-codes
country_df = pd.read_csv('https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/country_codes.csv', dtype = {'conuntry-code': str})
covid_df = covid_df.rename(columns = {'location':'Country'})
covid_df = covid_df.merge(country_df[['Country','country-code']],how='left', on=['Country'])

#world data
data_world = covid_df[covid_df['Country']=='World']

#country data
country_drop =  ['Africa', 'Asia', 'Europe', 'European Union', 'High income', 'International', 'Low income', 'Lower middle income', 'North America', 'Oceania', 'South America', 'Upper middle income', 'World']
data_country = covid_df.copy()
data_country = data_country[~pd.DataFrame(data_country.Country.tolist()).isin(country_drop).any(1).values]
"""
drop population < 500,000 (44)
"""


st.write("## COVID-19 cases of 2021")

#line plot global rate: 
"""
data_world
death/population, case/population, vaccinated/population
3 lines, legend
x - month
"""


#map countries:
"""
data_country
death, case, vaccination, population
3 maps, linked together, one country
x - month
"""
#selector month:




#bar plot: