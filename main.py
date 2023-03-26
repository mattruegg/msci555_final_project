import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import floor

pd.options.mode.chained_assignment = None

if __name__ == '__main__':
    artist_data = pd.read_csv('artist_data.csv')

    # artist_data.drop(index=67, inplace=True)
    # unscheduled_artists = []
    # unscheduled_artists = np.zeros(shape=(67, 4))

    weighting = []
    num_artist = len(artist_data)
    for x in range(num_artist):
        if x in artist_data['Artist']:
            y = artist_data.loc[x]
            weighting.append(y['ML'] / (y['SetLength']+15))

    unscheduled_artists = artist_data
    unscheduled_artists['Weighting'] = weighting
    # print(artist_data)
    # print(unscheduled_artists['Weighting'].idxmax())

    stage1 = []
    stage2 = []
    stage3 = []
    time1 = 0
    time2 = 0
    time3 = 0

    # stage order: 1 2 3 4 5 6 7 8 9
    w, h = 0, 9
    stages = [[0 for x in range(w)] for y in range(h)]
    genres = ['', '', '', '', '', '', '', '', '']
    times = [0, 0, 0, 50, 50, 50, 50, 50, 50]

    #
    # -------------------------- CREATE SCHEDULE --------------------------
    #

    for x in range(num_artist):
        choose_artist = unscheduled_artists.copy(deep=True)

        # choose a stage
        next_stage = times.index(min(times))

        # check for prev genre, reduce weight
        for y in range(len(choose_artist)):
            if y in artist_data['Artist']:
                z = choose_artist.loc[y]
                if z['Genre'] == genres[next_stage]:
                    choose_artist['Weighting'].loc[y] = (
                        z['ML'] / (z['SetLength'] + 5))

        # check for genre duplicate, increase weight
        for y in range(len(choose_artist)):
            if y in artist_data['Artist']:
                z = choose_artist.loc[y]
                if (1 < (z['Genre'] == genres[next_stage % 3])
                    + (z['Genre'] == (genres[next_stage % 3 + 3]))
                        + (z['Genre'] == (genres[next_stage % 3 + 6]))):
                    choose_artist['Weighting'].loc[y] /= 2

        # choose max WCT
        if next_stage >= 3:
            for y in choose_artist['Weighting'].nlargest(11).index.tolist():
                if choose_artist['ML'].loc[y] < 20000000:
                    next_artist = y
        else:
            next_artist = choose_artist['Weighting'].idxmax()

        # update stage vars
        if (choose_artist['Genre'].loc[next_artist] == genres[next_stage]):
            stages[next_stage].append([choose_artist['Artist'].loc[next_artist], 
                                        times[next_stage] - 10,
                                        choose_artist['SetLength'].loc[next_artist],
                                        times[next_stage] + choose_artist['SetLength'].loc[next_artist] - 10,
                                        choose_artist['Genre'].loc[next_artist]])
            times[next_stage] += choose_artist['SetLength'].loc[next_artist] + 5
        else:
            stages[next_stage].append([choose_artist['Artist'].loc[next_artist], 
                                        times[next_stage],
                                        choose_artist['SetLength'].loc[next_artist],
                                        times[next_stage] + choose_artist['SetLength'].loc[next_artist],
                                        choose_artist['Genre'].loc[next_artist]])
            times[next_stage] += choose_artist['SetLength'].loc[next_artist] + 15
        genres[next_stage] = choose_artist['Genre'].loc[next_artist]

        # remove from UA
        unscheduled_artists.drop(index=next_artist, inplace=True)

    print(times)
    # for x in stages:
    #     print(x)

    #
    # -------------------------- CREATE GRAPHS --------------------------
    #

    fig, gnt = plt.subplots()
    gnt.set_ylim(0, 90)
    gnt.set_xlim(0, 550)

    gnt.set_yticks([5, 15, 25, 35, 45, 55, 65, 75, 85])
    gnt.set_yticklabels(['Fri C', 'Fri O', 'Fri S', 'Sat C', 'Sat O', 'Sat S', 'Sun C', 'Sun O', 'Sun S'])

    for x in range(9):
        for y in stages[x]:
            gnt.broken_barh([(y[1], y[2])], ((((x%3)*3) + (floor(x/3)))*10, 9), ec='black')
            gnt.text(y[1] + 1, (((x%3)*3) + (floor(x/3)))*10 + 4, y[0], c='white', size='small')

    plt.show()
