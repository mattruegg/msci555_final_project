import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import floor
import random

pd.options.mode.chained_assignment = None


def colour_map(genre):
    match genre:
        case 'Alternative/Indie':
            return np.array([155, 0, 0])
        case 'Dance/Electronic':
            return np.array([175, 108, 0])
        case 'Hip-Hop/Rap':
            return np.array([155, 175, 0])
        case 'Latin/Mexican':
            return np.array([0, 170, 0])
        case 'Metal':
            return np.array([10, 10, 10])
        case 'Pop':
            return np.array([0, 10, 170])
        case 'R&B/Soul':
            return np.array([115, 0, 110])
        case 'Reggae':
            return np.array([150, 50, 110])
        case 'Rock':
            return np.array([0, 170, 70])

def create_graphs(times, stages):
    fig, gnt = plt.subplots()
    gnt.set_ylim(0, 90)
    gnt.set_xlim(0, max(times))

    gnt.set_yticks([5, 15, 25, 35, 45, 55, 65, 75, 85])
    gnt.set_yticklabels(['Fri C', 'Fri O', 'Fri S', 'Sat C',
                        'Sat O', 'Sat S', 'Sun C', 'Sun O', 'Sun S'])

    for x in range(9):
        for y in stages[x]:
            gnt.broken_barh([(y[1], y[2])], ((
                ((x % 3)*3) + (floor(x/3)))*10, 9), ec='black',
                facecolor=np.divide(colour_map(y[4]), 255).reshape(-1, 3))
            gnt.text(y[1] + 1, (((x % 3)*3) + (floor(x/3)))
                     * 10 + 4, y[0], c='white', size='small')

    plt.axhline(y=29.55, c='black')
    plt.axhline(y=59.58, c='black')

    plt.show()

def regular_scheulde(unscheduled_artists, base_changeover, fast_changeover):
    # stage order: 1 2 3 4 5 6 7 8 9
    w, h = 0, 9
    stages = [[0 for x in range(w)] for y in range(h)]
    genres = ['', '', '', '', '', '', '', '', '']
    times = [0-base_changeover, 0-base_changeover, 0-base_changeover, 
             50-base_changeover, 50-base_changeover, 50-base_changeover, 
             50-base_changeover, 50-base_changeover, 50-base_changeover]

    #
    # -------------------------- CREATE SCHEDULE --------------------------
    #

    for x in range(num_artist):
        choose_artist = unscheduled_artists.copy(deep=True)

        # choose a stage
        next_stage = times.index(min(times))

        # check for prev genre, reduce weight
        for y in range(68):
            if y in artist_data['Artist']:
                z = choose_artist.loc[y]
                if z['Genre'] == genres[next_stage]:
                    choose_artist['Weighting'].loc[y] = (
                        z['ML'] / (z['SetLength'] + fast_changeover))

        # check for genre duplicate, increase weight
        for y in range(68):
            if y in artist_data['Artist']:
                z = choose_artist.loc[y]
                if (next_stage <= 2 and
                    ((z['Genre'] == (genres[next_stage + 3]))
                     or (z['Genre'] == (genres[next_stage + 6])))):
                    choose_artist['Weighting'].loc[y] /= 2
                elif ((3 <= next_stage <= 5) and
                      ((z['Genre'] == (genres[next_stage + 3]))
                       or (z['Genre'] == (genres[next_stage - 3])))):
                    choose_artist['Weighting'].loc[y] /= 2
                elif ((6 <= next_stage <= 8) and
                      ((z['Genre'] == (genres[next_stage - 3]))
                       or (z['Genre'] == (genres[next_stage - 6])))):
                    choose_artist['Weighting'].loc[y] /= 2

        # choose max WCT
        if next_stage >= 3:
            for y in choose_artist['Weighting'].nlargest(15).index.tolist():
                if choose_artist['ML'].loc[y] < 20000000:
                    next_artist = y
                    break
        else:
            next_artist = choose_artist['Weighting'].idxmax()

        # update stage vars
        if (choose_artist['Genre'].loc[next_artist] == genres[next_stage]):
            stages[next_stage].append([choose_artist['Artist'].loc[next_artist],
                                       times[next_stage] + fast_changeover,
                                       choose_artist['SetLength'].loc[next_artist],
                                       times[next_stage]
                                       + choose_artist['SetLength'].loc[next_artist]
                                       + fast_changeover,
                                       choose_artist['Genre'].loc[next_artist],
                                       artist_data['NR'].loc[next_artist]])
            times[next_stage] += choose_artist['SetLength'].loc[next_artist] + fast_changeover
        else:
            stages[next_stage].append([choose_artist['Artist'].loc[next_artist],
                                       times[next_stage] + base_changeover,
                                       choose_artist['SetLength'].loc[next_artist],
                                       times[next_stage]
                                       + choose_artist['SetLength'].loc[next_artist]
                                       + base_changeover,
                                       choose_artist['Genre'].loc[next_artist],
                                       artist_data['NR'].loc[next_artist]])
            times[next_stage] += choose_artist['SetLength'].loc[next_artist] + base_changeover
        genres[next_stage] = choose_artist['Genre'].loc[next_artist]

        # remove from UA
        unscheduled_artists.drop(index=next_artist, inplace=True)

    # print(times)
    # for x in stages:
    #     print(x)

    weighted_sum = 0
    for x in stages:
        for y in x:
            weighted_sum += (y[5] * y[3])
    print(weighted_sum)

    #
    # -------------------------- CREATE GRAPHS --------------------------
    #

    create_graphs(times, stages)

    return

def random_schedule(unscheduled_artists, base_changeover, fast_changeover):
    # stage order: 1 2 3 4 5 6 7 8 9
    w, h = 0, 9
    stages = [[0 for x in range(w)] for y in range(h)]
    genres = ['', '', '', '', '', '', '', '', '']
    times = [0-base_changeover, 0-base_changeover, 0-base_changeover, 
             50-base_changeover, 50-base_changeover, 50-base_changeover, 
             50-base_changeover, 50-base_changeover, 50-base_changeover]

    #
    # -------------------------- CREATE SCHEDULE --------------------------
    #

    for x in range(num_artist):
        choose_artist = unscheduled_artists.copy(deep=True)

        # choose a stage
        next_stage = times.index(min(times))
        
        width = 15
        if next_stage >= 3:
            z = choose_artist['Weighting'].nlargest(width).index.tolist()
            next_artist = z[random.randint(0,len(z)-1)]
            while(choose_artist['ML'].loc[next_artist] > 20000000):
                print("if", z)
                next_artist = z[random.randint(0,len(z)-1)]
        else:
            z = choose_artist['Weighting'].nlargest(width).index.tolist()
            next_artist = z[random.randint(0,len(z)-1)]

        # update stage vars
        if (choose_artist['Genre'].loc[next_artist] == genres[next_stage]):
            stages[next_stage].append([choose_artist['Artist'].loc[next_artist],
                                       times[next_stage] + fast_changeover,
                                       choose_artist['SetLength'].loc[next_artist],
                                       times[next_stage]
                                       + choose_artist['SetLength'].loc[next_artist]
                                       + fast_changeover,
                                       choose_artist['Genre'].loc[next_artist],
                                       artist_data['NR'].loc[next_artist]])
            times[next_stage] += choose_artist['SetLength'].loc[next_artist] + fast_changeover
        else:
            stages[next_stage].append([choose_artist['Artist'].loc[next_artist],
                                       times[next_stage] + base_changeover,
                                       choose_artist['SetLength'].loc[next_artist],
                                       times[next_stage]
                                       + choose_artist['SetLength'].loc[next_artist]
                                       + base_changeover,
                                       choose_artist['Genre'].loc[next_artist],
                                       artist_data['NR'].loc[next_artist]])
            times[next_stage] += choose_artist['SetLength'].loc[next_artist] + base_changeover
        genres[next_stage] = choose_artist['Genre'].loc[next_artist]

        # remove from UA
        unscheduled_artists.drop(index=next_artist, inplace=True)

    # print(times)
    # for x in stages:
    #     print(x)

    weighted_sum = 0
    for x in stages:
        for y in x:
            weighted_sum += (y[5] * y[3])
    print(weighted_sum)

    #
    # -------------------------- CREATE GRAPHS --------------------------
    #

    # create_graphs(times, stages)

    return

if __name__ == '__main__':
    artist_data = pd.read_csv('artist_data.csv')

    base_changeover, fast_changeover = 20, 5

    weighting = []
    num_artist = len(artist_data)
    for x in range(num_artist):
        if x in artist_data['Artist']:
            y = artist_data.loc[x]
            weighting.append(y['ML'] / (y['SetLength'] + base_changeover))

    unscheduled_artists = artist_data
    unscheduled_artists['Weighting'] = weighting

    regular_scheulde(unscheduled_artists, base_changeover, fast_changeover)
    # random_schedule(unscheduled_artists, base_changeover, fast_changeover)
