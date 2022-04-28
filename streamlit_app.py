import altair as alt
import pandas as pd
import streamlit as st

covid_df = pd.read_csv('processed_data.csv')

#st.write("## COVID-19 cases from 2021 to 2022")

@st.cache
def load_data():
    ## {{ CODE HERE }} ##

    ### P1.2 ###
    # Move this code into `load_data` function {{
    cancer_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/cancer_ICD10.csv").melt(  # type: ignore
        id_vars=["Country", "Year", "Cancer", "Sex"],
        var_name="Age",
        value_name="Deaths",
    )

    pop_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/population.csv").melt(  # type: ignore
        id_vars=["Country", "Year", "Sex"],
        var_name="Age",
        value_name="Pop",
    )

    df = pd.merge(left=cancer_df, right=pop_df, how="left")
    df["Pop"] = df.groupby(["Country", "Sex", "Age"])["Pop"].fillna(method="bfill")
    df.dropna(inplace=True)

    df = df.groupby(["Country", "Year", "Cancer", "Age", "Sex"]).sum().reset_index()
    df["Rate"] = df["Deaths"] / df["Pop"] * 100_000

    # }}
    return df


# Uncomment the next line when finished
df = load_data()

### P1.2 ###

st.write("## Age-specific cancer mortality rates")

### P2.1 ###
# replace with st.slider
year = st.slider('Year', min_value=min(df['Year']), max_value=max(df['Year']),value=2012)
subset = df[df["Year"] == year]
### P2.1 ###


### P2.2 ###
# replace with st.radio
sex = st.radio('Sex', list(set(df.Sex)))
subset = subset[subset["Sex"] == sex]
### P2.2 ###