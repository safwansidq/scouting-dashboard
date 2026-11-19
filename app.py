from utils.data_processor import prepare_report
import streamlit as st

import math

#callback function
def reset_page():
    st.session_state.page = 0


st.set_page_config(page_title="scouting dashboard", layout="wide")

df = prepare_report()
filtered_df = df

st.sidebar.header('Filters')
leagues = sorted(df['Comp'].dropna().unique())
positions = sorted(df['PrimaryPos'].dropna().unique())

#search bar to find players names
chosen_player = st.sidebar.text_input('Player name', on_change=reset_page)
if chosen_player:
    mask = filtered_df['Player'].str.contains(
        chosen_player,
        case=False,
        na = False,
        regex=False
        )
    filtered_df = filtered_df[mask]
        

#multiselect for leagues
chosen_league = st.sidebar.multiselect('League', options = leagues, default = [], on_change=reset_page)
if chosen_league:
    filtered_df = filtered_df[filtered_df['Comp'].isin(chosen_league)]

#multiselect for Teams
teams = sorted(filtered_df['Squad'].dropna().unique())
chosen_team = st.sidebar.multiselect('Club Team', options = teams, default = [], on_change=reset_page)
if chosen_team:
    filtered_df = filtered_df[filtered_df['Squad'].isin(chosen_team)]

#multiselect for Positions
chosen_positions = st.sidebar.multiselect('positions', options = positions, default = [], on_change=reset_page)
if chosen_positions:
    filtered_df = filtered_df[filtered_df['PrimaryPos'].isin(chosen_positions)]

#slider for age
age_min, age_max = st.sidebar.slider('Age', 16, 40, (18, 30), on_change=reset_page)
filtered_df = filtered_df[(filtered_df['Age'] >= age_min) & (filtered_df['Age'] <= age_max)]

#slider for minutes played
min_min, min_max = st.sidebar.slider('Min', 900, 3420, (1200, 2500), on_change=reset_page)
filtered_df = filtered_df[(filtered_df['Min'] >= min_min) & (filtered_df['Min'] <= min_max)]

#if no players matched
if len(filtered_df) == 0:
    st.warning('No Players Matched')
    st.stop()


#options to change page sizes
page_size = st.selectbox('Rows per page', options =[10, 25, 50], index = 0, on_change=reset_page)

#page is kept unchanged after reruns
if 'page' not in st.session_state:
    st.session_state.page = 0

#buttons that change pages
col1, col2 = st.columns(2)
with col1:
    if st.button('Previous'):
        st.session_state.page -= 1

with col2:
    if st.button('Next'):
        st.session_state.page += 1

#guard rails
total_pages = math.ceil(len(filtered_df) / page_size)
st.session_state.page = max(0, min(st.session_state.page, total_pages - 1))

#slicing the dataframe
start = st.session_state.page * page_size
end = start + page_size
sorted_df = filtered_df.sort_values(by = 'overall_percentile', ascending = False)
page_df = sorted_df.iloc[start:end]

#working code
mini = page_df[['Player', 'Squad', 'PrimaryPos', 'Age', 'Min', 'npxG_per90', 'xA_per90', 'PrgP_per90', 'overall_percentile']]

#renaming the columns to make it more readable
mini = mini.rename(columns={
    'Squad': 'Club',
    'PrimaryPos': 'Position',
    'Min': 'Minutes',
    'npxG_per90': 'Non Penalty xG per 90',
    'xA_per90': 'xA per 90',
    'PrgP_per90': 'Progressive Passes per 90',
    'overall_percentile': 'Overall Percentile'
})
mini = mini.round(2)
st.title('Filtered Team')
st.write('players matched: ', len(filtered_df))
st.dataframe(mini, hide_index=True)

st.write(f'Page: {st.session_state.page + 1} out of {total_pages}')







