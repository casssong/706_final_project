import altair as alt
import pandas as pd
import streamlit as st
from vega_datasets import data

alt.data_transformers.disable_max_rows()

@st.cache

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
# Map - total cases, total deaths
df_map = data_country.groupby(['Country', 'total_cases', 'total_deaths','population','year']).sum().reset_index()
#df2['Rate'] = df2['Death']/df2['Pop'] * 1000000
source = alt.topo_feature(data.world_110m.url, 'countries')
year = 2021 # only visualize for 2021
data_country = data_country[data_country['year']==year]
width = 600
height  = 300
project = 'equirectangular'


# a gray map using as the visualization background
background = alt.Chart(source
                       ).mark_geoshape(
    fill='#aaa',
    stroke='white'
).properties(
    width=width,
    height=height
).project(project)


selector = alt.selection_single(
    fields=['id']
)


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

# fix the color schema so that it will not change upon user selection
case_scale = alt.Scale(domain=[df_map['total_cases'].min(), df_map['total_cases'].max()])
case_color = alt.Color(field="total_cases", type="quantitative", scale=case_scale)
chart_case = chart_base.mark_geoshape().encode(
    ######################
    # P3.1 map visualization showing the mortality rate
    color=case_color,
    ######################
    # P3.3 tooltip
    tooltip= ['total_cases:Q', 'Country:N']
).transform_filter(
    selector
).properties(
    title=f'Total Cases Worldwide {year}'
)

#selector month:




#bar plot: