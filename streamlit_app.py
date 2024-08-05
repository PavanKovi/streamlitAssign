import streamlit as st
import pandas as pd
import io
import requests
import altair as alt

# Load the data
@st.cache
def load_data():
    url = 'https://drive.google.com/uc?export=download&id=1ePNeKEvPc_l6SWBcvH-MK0Y8eyu3GapR'
    response = requests.get(url)
    data = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
    return data

data = load_data()

# Title
st.title("Olympic Athletes Data Analysis")

# Display the raw data
if st.checkbox("Show raw data"):
    st.write(data)

# Sidebar for user input
st.sidebar.header("Filter options")

# Filter by Year
years = data['Year'].unique()
selected_year = st.sidebar.multiselect("Select Year(s)", years, default=years)

# Filter by Sport
sports = data['Sport'].unique()
selected_sport = st.sidebar.multiselect("Select Sport(s)", sports, default=sports)

# Filter by Sex
sex = data['Sex'].unique()
selected_sex = st.sidebar.multiselect("Select Sex", sex, default=sex)

# Filter the data based on user input
filtered_data = data[(data['Year'].isin(selected_year)) & 
                     (data['Sport'].isin(selected_sport)) &
                     (data['Sex'].isin(selected_sex))]

st.write(f"Filtered Data: {len(filtered_data)} rows")
st.write(filtered_data)

# Plotting
st.header("Medal Distribution")

# Medal count per team
medal_count = filtered_data.groupby(['Team', 'Medal']).size().unstack(fill_value=0)
st.bar_chart(medal_count)

# Medal count per sport
medal_count_sport = filtered_data.groupby(['Sport', 'Medal']).size().unstack(fill_value=0)
st.bar_chart(medal_count_sport)

# Medal count per year
medal_count_year = filtered_data.groupby(['Year', 'Medal']).size().unstack(fill_value=0)
st.line_chart(medal_count_year)

# Additional analysis
st.header("Additional Analysis")

# Age distribution
st.subheader("Age Distribution")
age_hist = alt.Chart(filtered_data.dropna(subset=['Age'])).mark_bar().encode(
    alt.X("Age:Q", bin=True),
    y='count()',
).properties(
    width=600,
    height=400
)
st.altair_chart(age_hist)

# Height distribution
st.subheader("Height Distribution")
height_hist = alt.Chart(filtered_data.dropna(subset=['Height'])).mark_bar().encode(
    alt.X("Height:Q", bin=True),
    y='count()',
).properties(
    width=600,
    height=400
)
st.altair_chart(height_hist)

# Weight distribution
st.subheader("Weight Distribution")
weight_hist = alt.Chart(filtered_data.dropna(subset=['Weight'])).mark_bar().encode(
    alt.X("Weight:Q", bin=True),
    y='count()',
).properties(
    width=600,
    height=400
)
st.altair_chart(weight_hist)
