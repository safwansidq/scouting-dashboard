from utils.data_processor import prepare_report
import streamlit as st

st.set_page_config(page_title="scouting dashboard", layout="wide")

df = prepare_report()
filtered_df = df

st.sidebar.header('Filters')
leagues = sorted(df['Comp'].dropna().unique())
teams = sorted(df['Squad'].dropna().unique())
positions = sorted(df['PrimaryPos'].dropna().unique())

#multiselect for leagues
chosen_league = st.sidebar.multiselect('League', options = leagues, default = leagues)
filtered_df = df[df['Comp'].isin(chosen_league)]

#multiselect for Teams
chosen_team = st.sidebar.multiselect('Club Team', options = teams, default = teams)
filtered_df = filtered_df[filtered_df['Squad'].isin(chosen_team)]

#multiselect for Positions
chosen_positions = st.sidebar.multiselect('positions', options = positions, default = positions)
filtered_df = filtered_df[filtered_df['PrimaryPos'].isin(chosen_positions)]

#slider for age
age_min, age_max = st.sidebar.slider('Age', 16, 40, (18, 30))
filtered_df = filtered_df[(filtered_df['Age'] >= age_min) & (filtered_df['Age'] <= age_max)]

#slider for minutes played
min_min, min_max = st.sidebar.slider('Min', 900, 3420, (1200, 2500))
filtered_df = filtered_df[(filtered_df['Min'] >= min_min) & (filtered_df['Min'] <= min_max)]

mini = filtered_df[['Player', 'PrimaryPos', 'overall_percentile']]
mini = mini.sort_values(by = 'overall_percentile', ascending = False)
st.title('Filtered Team')
st.write('Rows', len(filtered_df))
st.dataframe((mini.head(10)))

