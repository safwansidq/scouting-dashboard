from utils.data_processor import prepare_report
import streamlit as st

import math

st.set_page_config(page_title="scouting dashboard", layout="wide")

df = prepare_report()
filtered_df = df

st.sidebar.header('Filters')
leagues = sorted(df['Comp'].dropna().unique())
teams = sorted(df['Squad'].dropna().unique())
positions = sorted(df['PrimaryPos'].dropna().unique())

#options to change page sizes
page_size = st.selectbox('Rows per page', options =[10, 25, 50], index = 0)

if 'page' not in st.session_state:
    st.session_state.page = 0

#slicing the dataframe
start = page * page_size
end = start + page_size
page_df = sorted_df.iloc[start:end]

#buttons that change pages
col1, col2 = st.columns(2)
with col1:
    if st.button('Previous'):
        st.session_state.page -= 1

with col2:
    if st.button('Next'):
        st.session_state.page += 1
        

#guard rails
total_pages = math.ceil(len(sorted_df) / page_size)
page = max(0, min(page, total_pages - 1))

#multiselect for leagues
chosen_league = st.sidebar.multiselect('League', options = leagues, default = [])
if chosen_league:
    filtered_df = df[df['Comp'].isin(chosen_league)]

#multiselect for Teams
chosen_team = st.sidebar.multiselect('Club Team', options = teams, default = [])
if chosen_team:
    filtered_df = filtered_df[filtered_df['Squad'].isin(chosen_team)]

#multiselect for Positions
chosen_positions = st.sidebar.multiselect('positions', options = positions, default = [])
if chosen_positions:
    filtered_df = filtered_df[filtered_df['PrimaryPos'].isin(chosen_positions)]

#slider for age
age_min, age_max = st.sidebar.slider('Age', 16, 40, (18, 30))
filtered_df = filtered_df[(filtered_df['Age'] >= age_min) & (filtered_df['Age'] <= age_max)]

#slider for minutes played
min_min, min_max = st.sidebar.slider('Min', 900, 3420, (1200, 2500))
filtered_df = filtered_df[(filtered_df['Min'] >= min_min) & (filtered_df['Min'] <= min_max)]

mini = filtered_df[['Player', 'Squad', 'PrimaryPos', 'overall_percentile']]
mini = mini.sort_values(by = 'overall_percentile', ascending = False)
st.title('Filtered Team')
st.write('Rows', len(filtered_df))
st.dataframe((mini.head(50)))

