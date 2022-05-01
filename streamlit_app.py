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
df_line = data_world.copy()
df_line = pd.melt(df_line, id_vars=['Country','month'], value_vars=['total_cases', 'total_deaths','people_vaccinated'], var_name = "Global_data", value_name='value')
df_line['Global_data'] = df_line['Global_data'].map({'total_cases':'Total Cases',
                                                     'total_deaths': 'Total Deaths',
                                                     'people_vaccinated': 'People Vaccinated'})
data_selection = alt.selection_single(
    fields=["Global_data"], bind='legend'
)
chart_line = alt.Chart(df_line).mark_line().encode(
    x = alt.X('month:N', title='Month'),
    y = alt.Y('sum(value)', title="Total Number of People"),
    color = alt.condition(data_selection, "Global_data", alt.value('lightgray'), legend=alt.Legend(title="Data Type")),
    tooltip=[alt.Tooltip("month", title="Month"), alt.Tooltip("value:Q", title='Number of People')]
).add_selection(
    data_selection
).properties(
    width=750,
    height=400
)
st.altair_chart(chart_line)

#map countries:
# data_country
# death, case, vaccination, population
# 3 maps, linked together, one country
# x - month
st.write("### Choropleth Map of Population and COVID-19 related statistics")
# Map - total cases, total deaths
df_map = data_country.groupby(['Country','people_vaccinated' ,'total_cases', 'total_deaths','population','year']).sum().reset_index()
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
        from_=alt.LookupData(df_map, "country-code", ['people_vaccinated', "total_cases", 'Country', 'total_deaths','population' ,'year']),
    )

# fix the color schema so that it will not change upon user selection
case_scale = alt.Scale(domain=[df_map['total_cases'].min(), df_map['total_cases'].max()])
case_color = alt.Color(field="total_cases", type="quantitative", scale=case_scale, legend=alt.Legend(title="Total Cases"))
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
    title=f'Total Cases Worldwide 2021'
)

# fix the color schema so that it will not change upon user selection
death_scale = alt.Scale(domain=[df_map['total_deaths'].min(), df_map['total_deaths'].max()])
death_color = alt.Color(field="total_deaths", type="quantitative", scale=death_scale, legend=alt.Legend(title="Total Death"))
chart_death = chart_base.mark_geoshape().encode(
    ######################
    # P3.2 map visualization showing the mortality rate
    color=death_color,
    ######################
    # P3.3 tooltip
    tooltip= ['total_deaths:Q', 'Country:N']
).transform_filter(
    selector
).properties(
    title=f'Total Deaths Worldwide 2021'
)


chart_map = alt.vconcat(background + chart_case, background + chart_death
                        ).resolve_scale(
    color='independent'
)

st.altair_chart(chart_map)


#bar plot:
df_bar = data_country[['Country','month','total_cases', 'people_vaccinated','stringency_index','population']]
df_bar['policy_score'] = df_bar['stringency_index'] * 100000
df_bar = pd.melt(df_bar, id_vars=['Country','month'], value_vars=['total_cases', 'people_vaccinated','policy_score'], var_name = "Data", value_name='value')

#df_bar = data_country[['Country','month','total_cases', 'people_vaccinated','stringency_index']]
#df_bar = df_bar.rename(columns={'stringency_index': 'policy_score'}) 
#df_bar = pd.melt(df_bar, id_vars=['Country','month'], value_vars=['total_cases', 'people_vaccinated','policy_score'], var_name = "Data", value_name='value')


#select month:
month = st.slider('Month', 1,12,4,1)
subset = df_bar[df_bar["month"] == month]
#select countries:
countries = st.multiselect('Countries', df_bar['Country'].unique())
subset = subset[subset["Country"].isin(countries)]
#bar plot

data_selection = alt.selection_single(
    fields=["Data"], bind='legend'
)
chart_bar = alt.Chart(subset).mark_bar().encode(
    x = alt.X("Data", title='Data'),
    y = alt.Y('sum(value)', title="Value"),
    color = alt.condition(data_selection, "Data", alt.value('lightgray')),
    tooltip=["Country","value"]
).add_selection(
    data_selection
).properties(
    title='Policy Score'
).facet(
    column = alt.Column('Country:N')
).properties(
    title='Comparison Between Countries'
)

st.altair_chart(chart_bar)