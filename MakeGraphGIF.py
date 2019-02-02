#Create Animation Graph as gif file
import pandas as pd
import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import json
import codecs

if __name__ == '__main__':
    f = open("init.json", 'r')
    json_data = json.load(f)

    fileName = json_data['file']
    playerA = json_data['playera']
    playerB = json_data['playerb']
    set1 = json_data['set1']
    set2 = json_data['set2']
    set3 = json_data['set3']

    with codecs.open(fileName, "r", "SJIS", "ignore") as file:
        df = pd.read_table(file, delimiter=",")
    df['FirstSecond'] = df['FirstSecond'].convert_objects(
        convert_numeric=True).fillna(-1).astype(np.int)
    df = df.reset_index()

    flow_array = np.loadtxt(fileName + "_output.csv", delimiter=",")
    gameA_array = np.loadtxt(fileName + "_gamea.csv", delimiter=",")
    gameB_array = np.loadtxt(fileName + "_gameb.csv", delimiter=",")
    plen = len(flow_array)


    temp1 = []
    temp2 = []
    for i in range(len(flow_array)):
        temp1.append(flow_array[i][0])
        temp2.append(flow_array[i][1])

    y1 = np.array(temp1)
    y2 = np.array(temp2)
    x = np.array(range(len(flow_array)))

    fig = plt.figure()

    df['diff'] = (df['Set'] - df['Set'].shift(1)).fillna(0)
    df_temp = df[df['diff'] == 1].index

    ims = []
    for i in range(1, len(flow_array)):
        im1, = plt.plot(x[:i], y1[:i], "deepskyblue")
        im2, = plt.plot(x[:i], y2[:i], "orange")
        if(i <= df_temp[0]):
            s1 = 'GAME%d-%d' % (gameA_array[i], gameB_array[i])
            s2 = ''
            s3 = ''
        elif(i > df_temp[0] and i <= df_temp[1]):
            s1 = 'GAME ' + set1
            s2 = 'GAME %d-%d' % (gameA_array[i], gameB_array[i])
            s3 = ''
        elif(i > df_temp[1]):
            s1 = 'GAME ' + set1
            s2 = 'GAME ' + set2
            s3 = 'GAME %d-%d' % (gameA_array[i], gameB_array[i])
        else:
            s1 = 'GAME ' + set1
            s2 = 'GAME ' + set2
            s3 = 'GAME ' + set3
        im3 = plt.text(
            0,
            80,
            s1,
            ha='left',
            va='bottom',
            color='blue',
            fontsize=16)
        im4 = plt.text(
            df_temp[0],
            80,
            s2,
            ha='left',
            va='bottom',
            color='blue',
            fontsize=16)
        im5 = plt.text(
            df_temp[1],
            80,
            s3,
            ha='left',
            va='bottom',
            color='blue',
            fontsize=16)

        ims.append([im1, im2, im3, im4, im5])

    for i, d in enumerate(df_temp):
        plt.plot([d, d], [-10, 110], "blue", linestyle='dashed')  # SETの境界線
        plt.text(
            d,
            90,
            'SET%d' % (i + 2),
            ha='left',
            va='bottom',
            color='blue',
            fontsize=16)

    plt.grid(which='major', color='gray', linestyle='-')
    plt.text(0, 90, 'SET1', ha='left', va='bottom', color='blue', fontsize=16)

    plt.title(
        "Win Probability Simulation @DataTennis.Net\n" +
        playerA +
        " vs " +
        playerB)
    plt.xlabel("nthPoint", fontsize=18)
    plt.ylabel("Win Probability %", fontsize=18)

    plt.xlim([0, plen])
    plt.ylim([0, 100])

    plt.legend([playerA, playerB], fontsize=14, loc='center')

    ani = animation.ArtistAnimation(fig, ims, interval=200)  # 33
    ani.save(fileName + '_graph.gif', writer='imagemagick')
