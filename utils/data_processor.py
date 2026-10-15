#load the csv

#work out each player's primary position

#apply your filter (15 appearances and 900 minutes)

#calculate per-90 stats

#calculate percentiles within each position

#calculate the weighted score

#turn the score into an overall percentile

import pandas as pd 

DATA_PATH = "data/players_data-2024_2025.csv"

def load_data(path):
    '''this function loads the data from the csv file'''
    df = pd.read_csv(path)
    return df

if __name__ == "__main__":
    df = load_data(DATA_PATH)
    print(df['Comp'].nunique())
 
    print(df.shape)

