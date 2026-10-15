#load the csv
import pandas as pd 

DATA_PATH = "data/players_data-2024_2025.csv"

def load_data(path):
    '''this function loads the data from the csv file'''
    df = pd.read_csv(path)
    return df

#work out each player's primary position
def add_primary_position(df):
    '''this function takes the primary position of the player from the possible positions he has played'''
    df = df.copy()
    df['PrimaryPos'] = df['Pos'].str.split(',').str[0]
    return df

#apply your filter (15 appearances and 900 minutes)
def filter_players(df):
    '''this function filters the players based on the number of appearances and minutes played'''
    df = df.copy()
    filtered_df = df[(df['MP'] >= 15) & (df['Min'] >= 900)]
    return filtered_df

#calculate per-90 stats
def add_per90_stats(df):
    '''this function converts the metrics into per-90 stats'''
    df = df.copy()
    df['npxG_per90'] = (df['npxG'] / df['Min']) * 90  #npxG per 90 minutes
    df['xA_per90'] = (df['xA'] / df['Min']) * 90  #xA per 90 minutes
    df['PrgP_per90'] = (df['PrgP'] / df['Min']) * 90  #PrgP per 90 minutes
    return df

#calculate percentiles within each position

#calculate the weighted score

#turn the score into an overall percentile



if __name__ == "__main__":
    df = load_data(DATA_PATH)
    print(df['Comp'].nunique())
    print(df.shape)
    df = add_primary_position(df)
    print(df['PrimaryPos'].value_counts())
    df = filter_players(df)
    print(df.shape)
    df = add_per90_stats(df)
    print(df['npxG_per90'].mean().round(2)) 

