#load the csv
import pandas as pd 

DATA_PATH = "data/players_data-2024_2025.csv"
WEIGHTS = {
    'FW': {'npxG_per90_pct': 0.5, 'xA_per90_pct': 0.3, 'PrgP_per90_pct': 0.2},
    'MF': {'npxG_per90_pct': 0.2, 'xA_per90_pct': 0.3, 'PrgP_per90_pct': 0.5},
    'DF': {'npxG_per90_pct': 0.15, 'xA_per90_pct': 0.15, 'PrgP_per90_pct': 0.7},
    'GK': {'npxG_per90_pct': 0.2, 'xA_per90_pct': 0.2, 'PrgP_per90_pct': 0.6}
}

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
def add_percentililes(df):
    '''this function calculates the percentiles for the per-90 stats'''
    df = df.copy()
    df['npxG_per90_pct'] = df.groupby('PrimaryPos')['npxG_per90'].rank(pct=True) * 100
    df['xA_per90_pct'] = df.groupby('PrimaryPos')['xA_per90'].rank(pct=True) * 100
    df['PrgP_per90_pct'] = df.groupby('PrimaryPos')['PrgP_per90'].rank(pct=True) * 100
    return df

#calculate the weighted score
def overall_score(df):
    '''this function calculates the overall score for the players'''
    df = df.copy()
    df['overall_score'] = 0.0
    FW = df['PrimaryPos'] == 'FW'
    MF = df['PrimaryPos'] == 'MF'
    DF = df['PrimaryPos'] == 'DF'
    GK = df['PrimaryPos'] == 'GK'

    df.loc[FW, 'overall_score'] = (
        df.loc[FW, 'npxG_per90_pct'] * WEIGHTS['FW']['npxG_per90_pct'] +
        df.loc[FW, 'xA_per90_pct'] * WEIGHTS['FW']['xA_per90_pct'] +
        df.loc[FW, 'PrgP_per90_pct'] * WEIGHTS['FW']['PrgP_per90_pct']
    )
    df.loc[MF, 'overall_score'] = (
        df.loc[MF, 'npxG_per90_pct'] * WEIGHTS['MF']['npxG_per90_pct'] +
        df.loc[MF, 'xA_per90_pct'] * WEIGHTS['MF']['xA_per90_pct'] +
        df.loc[MF, 'PrgP_per90_pct'] * WEIGHTS['MF']['PrgP_per90_pct']
    )
    df.loc[DF, 'overall_score'] = (
        df.loc[DF, 'npxG_per90_pct'] * WEIGHTS['DF']['npxG_per90_pct'] +
        df.loc[DF, 'xA_per90_pct'] * WEIGHTS['DF']['xA_per90_pct'] +
        df.loc[DF, 'PrgP_per90_pct'] * WEIGHTS['DF']['PrgP_per90_pct']
    )
    df.loc[GK, 'overall_score'] = (
        df.loc[GK, 'npxG_per90_pct'] * WEIGHTS['GK']['npxG_per90_pct'] +
        df.loc[GK, 'xA_per90_pct'] * WEIGHTS['GK']['xA_per90_pct'] +
        df.loc[GK, 'PrgP_per90_pct'] * WEIGHTS['GK']['PrgP_per90_pct']
    )
    return df

#turn the score into an overall percentile
def overall_percentile(df):
    '''this function turns the score into an overall percentile'''
    df = df.copy()
    df['overall_percentile'] = df.groupby('PrimaryPos')['overall_score'].rank(pct = True) * 100
    return df

def prepare_report(path = DATA_PATH):
    df = load_data(path)
    df = add_primary_position(df)
    df = filter_players(df)
    df = add_per90_stats(df)
    df = add_percentililes(df)
    df = overall_score(df)
    df = overall_percentile(df)
    return df
if __name__ == "__main__":
    df = prepare_report()
    print(df.head(10))
    mini = df[['Player', 'PrimaryPos', 'overall_percentile']]
    mini = mini.sort_values(by='overall_percentile', ascending=False)
    mini = mini[mini['PrimaryPos'] == 'FW']
    print(mini.head(10))
