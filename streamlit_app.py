import altair as alt
import pandas as pd
import streamlit as st
from vega_datasets import data

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

#drop population < 500,000 (44)
drop_lowpop = data_country[data_country['population'] < 500000]['Country'].unique()
data_country = data_country[~pd.DataFrame(data_country.Country.tolist()).isin(drop_lowpop).any(1).values]


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

# Map - total cases, total deaths
df_map = data_country.groupby(['Country', 'total_cases', 'total_deaths','population','year']).sum().reset_index()
source = alt.topo_feature(data.world_110m.url, 'countries')
width = 600
height  = 300
project = 'equirectangular'

# a gray map using as the visualization background
background = alt.Chart(source).mark_geoshape(
    fill='#aaa',
    stroke='white'
).properties(
    width=width,
    height=height
).project(project)

selector = alt.selection_single(fields=['id'])

chart_base = alt.Chart(source
    ).properties(
        width=width,
        height=height
    ).project(project
    ).add_selection(selector
    ).transform_lookup(
        lookup="id",
        from_=alt.LookupData(df_map, "country-code", ["total_cases", 'Country', 'total_deaths','population' ,'year']),
    )
#selector month:




#bar plot: