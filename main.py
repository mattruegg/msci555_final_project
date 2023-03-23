import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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
            # z = [y["Artist"], y['SetLength'], y['NR'], y['SetLength'] * y['NR']]
            # unscheduled_artists.append(z)
            weighting.append(y['SetLength'] * y['NR'])

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

    for x in range(num_artist):
        y = unscheduled_artists['Weighting'].idxmax()
        if (time1 <= time2 and time1 <= time3) or artist_data['MonthlyListeners'].loc[y] > 20000000:
            stage1.append([y, artist_data['Artist'].loc[y],
                          artist_data['SetLength'].loc[y], time1])
            time1 += artist_data['SetLength'].loc[y]
        elif time2 <= time3:
            stage2.append([y, artist_data['Artist'].loc[y],
                          artist_data['SetLength'].loc[y], time2])
            time2 += artist_data['SetLength'].loc[y]
        else:
            stage3.append([y, artist_data['Artist'].loc[y],
                          artist_data['SetLength'].loc[y], time3])
            time3 += artist_data['SetLength'].loc[y]
        artist_data.drop(index=y, inplace=True)

    # print(time1, time2, time3)
    # print("Stage 1")
    # for x in stage1:
    #     print (x)
    # print("Stage 2")
    # for x in stage2:
    #     print (x)
    # print("Stage 3")
    # for x in stage3:
    #     print (x)

    fig, gnt = plt.subplots()
    gnt.set_ylim(10, 40)
    gnt.set_xlim(0, 1090)

    gnt.set_yticks([15, 25, 35])
    gnt.set_yticklabels(['3', '2', '1'])

    for x in stage1:
        c = np.array([0, 0])
        gnt.broken_barh([(x[3], x[2])], (30, 9),
                        facecolor=np.append(c, (np.random.rand()+1)/2), ec='black')
        gnt.text(x[3] + 10, 30.5, x[1], rotation='vertical',
                 c='white', size='small')
    for x in stage2:
        c = np.array([0])
        c = np.append(c, (np.random.rand()+1)/2)
        gnt.broken_barh([(x[3], x[2])], (20, 9),
                        facecolor=np.append(c, 0), ec='black')
        gnt.text(x[3] + 10, 20.5, x[1], rotation='vertical',
                 c='black', size='small')
    for x in stage3:
        c = np.array([0, 0])
        gnt.broken_barh([(x[3], x[2])], (10, 9),
                        facecolor=np.append((np.random.rand()+1)/2, c), ec='black')
        gnt.text(x[3] + 10, 10.5, x[1], rotation='vertical',
                 c='white', size='small')

    plt.show()
