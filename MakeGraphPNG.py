#Create Graph as png file
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import codecs

if __name__ == '__main__':
    f = open("init.json", 'r')
    json_data = json.load(f)

    fileName = json_data['file']
    playerA = json_data['playera']
    playerB = json_data['playerb']

    with codecs.open(fileName, "r", "SJIS", "ignore") as file:
        df = pd.read_table(file, delimiter=",")
    df['FirstSecond'] = df['FirstSecond'].convert_objects(
        convert_numeric=True).fillna(-1).astype(np.int)
    df = df.reset_index()

    flow_array = np.loadtxt(fileName + "_output.csv", delimiter=",")
    plen = len(flow_array)

    plt.plot(flow_array)

    df['diff'] = (df['Set'] - df['Set'].shift(1)).fillna(0)
    df_temp = df[df['diff'] == 1].index
    for i, d in enumerate(df_temp):
        plt.plot([d, d], [-10, 110], "blue", linestyle='dashed')
        plt.text(
            d,
            90,
            'set%d' % (i + 2),
            ha='left',
            va='bottom',
            color='blue',
            fontsize=16)

    plt.grid(which='major', color='gray', linestyle='-')
    plt.text(0, 90, 'set1', ha='left', va='bottom', color='blue', fontsize=16)

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
    plt.savefig(fileName + '_graph.png')
