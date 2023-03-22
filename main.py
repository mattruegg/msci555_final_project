import pandas as pd

if __name__ == '__main__':
    artist_data = pd.read_csv('artist_data.csv')

    for x in range(len(artist_data)):
        print(artist_data.loc[x, 'Name'])
