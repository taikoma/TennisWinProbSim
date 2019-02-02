#This Script is for Win Probability Simulation
#Before simulating,You need to edit the init.json

import pandas as pd
import numpy as np
import codecs
import sys
import json


def isServeIn(perServeIn, serve):
    return np.random.randint(0, 100) < perServeIn[serve]


def addGamePoint(perServe, serve, gamePoint, numServe, totalServe):
    totalServe[serve] += 1
    winlose = np.random.randint(0, 100) < perServe[serve]  # 0～99
    if(winlose):
        gamePoint[serve] += 1
        numServe[serve] += 1
    else:
        gamePoint[(serve + 1) % 2] += 1
    return gamePoint


def returnGameNext(gamePoint, serve, game):
    for i in range(2):
        if(gamePoint[i] > 3 and (gamePoint[i] - gamePoint[(i + 1) % 2]) > 1):
            game[i] += 1
            serve = (serve + 1) % 2
            gamePoint[0] = 0
            gamePoint[1] = 0
    return gamePoint, serve, game


def returnTiebreakNext(gameNum, gamePoint, serve, game, status, gameLog, sets):
    for i in range(2):
        if(gamePoint[i] > 6 and (gamePoint[i] - gamePoint[(i + 1) % 2]) > 1):
            status = 0
            game[i] += 1
            serve = (serve + 1) % 2
            gamePoint[0] = 0
            gamePoint[1] = 0

            gameLog.append([gameNum, game[0], game[1]])
            sets[i] += 1
            game[0] = 0
            game[1] = 0

    return gamePoint, serve, game, status, gameLog, sets


def returnSetNext(gameNum, game, serve, sets, status, gameLog):
    if((sets[0] + sets[1]) < 4 and game[0] == 6 and game[1] == 6):
        status = 1
    else:
        for i in range(2):
            if(game[i] > 5 and (game[i] - game[(i + 1) % 2]) > 1):
                gameLog.append([gameNum, game[0], game[1]])
                sets[i] += 1
                serve = (serve + 1) % 2
                game[0] = 0
                game[1] = 0
    return game, serve, sets, status, gameLog


def returnFinishNext(serve, sets, status, gameWon_array, setLog, setMatch):
    for i in range(2):
        if(sets[i] > setMatch - 1):
            setLog.append([sets[0], sets[1]])
            gameWon_array[i] += 1
            status = 2
    return status, gameWon_array, setLog


def createList(dftemp):
    list = [
        dftemp["1st Serve"],
        dftemp["1st Serve Points Won"],
        dftemp["2nd Serve Points Won"],
        dftemp["1st Serve Return Points Won"],
        dftemp["2nd Serve Return Points Won"]]
    return list


def calcWonPer(
        per1stServeIn,
        per2ndServeIn,
        p1_1,
        s1_1,
        p1_2,
        s1_2,
        p2_1,
        s2_1,
        p2_2,
        s2_2,
        numGames,
        gamePoint_start,
        game_start,
        sets_start):
    anderson = np.array([71, 84, 59, 22, 41])

    s = 0
    perGame_array = []
    stats_array = []

    num1stServe = [0, 0]
    num2ndServe = [0, 0]
    total1stServe = [0, 0]
    total2ndServe = [0, 0]
    gameWon_array = [0, 0]
    gameLog = []
    setLog = []

    for i in range(numGames):
        num1stServe = [0, 0]
        num2ndServe = [0, 0]
        total1stServe = [0, 0]
        total2ndServe = [0, 0]
        status = 0
        gamePoint = gamePoint_start[:]
        game = game_start[:]
        sets = sets_start[:]

        serve = np.random.randint(0, 2)
        dist1_1 = np.random.normal(p1_1, s1_1)
        dist2_1 = np.random.normal(p2_1, s2_1)
        dist1_2 = np.random.normal(p1_2, s1_2)
        dist2_2 = np.random.normal(p2_2, s2_2)

        per1stServe = [dist1_1, dist2_1]
        per2ndServe = [dist1_2, dist2_2]

        while status < 2:
            if(isServeIn(per1stServeIn, serve)):
                gamePoint = addGamePoint(
                    per1stServe, serve, gamePoint, num1stServe, total1stServe)
            else:
                if(isServeIn(per2ndServeIn, serve)):
                    gamePoint = addGamePoint(
                        per2ndServe, serve, gamePoint, num2ndServe, total2ndServe)
                else:
                    gamePoint[(serve + 1) % 2] += 1

            if(status == 1):
                gamePoint, serve, game, status, gameLog, sets = returnTiebreakNext(
                    i, gamePoint, serve, game, status, gameLog, sets)
            elif(status == 0):
                gamePoint, serve, game = returnGameNext(gamePoint, serve, game)

            game, serve, sets, status, gameLog = returnSetNext(
                i, game, serve, sets, status, gameLog)
            status, gameWon_array, setLog = returnFinishNext(
                serve, sets, status, gameWon_array, setLog, 2)

    wonPerA, wonPerB = round(
        gameWon_array[0] / numGames * 100, 1), round(gameWon_array[1] / numGames * 100, 1)
    return wonPerA, wonPerB


def calcPer(np_pointList):
    per = np.count_nonzero(np_pointList) * 100.0 / len(np_pointList)
    return per


def inOut(np_pointList, a):
    # pointList.pop(0)######todo numpy方式に変換
    np_pointList = np.delete(np_pointList, 0)
    np_pointList = np.append(np_pointList, a)  # pointList.append(a)
    return np_pointList


def calcPoint(ab1, ab2, df, serveIn, point_1st, point_2nd, gamePoint):  # ab1=1 Aのポイント ab2=1 Bのポイント
    gamePoint[ab2] += 1
    if(int(df['FirstSecond'][i]) == 1):
        serveIn = inOut(serveIn, 1)
        point_1st = inOut(point_1st, ab1)
    elif(int(df['FirstSecond'][i]) == 2):
        point_2nd = inOut(point_2nd, ab1)
    return point_1st, point_2nd


if __name__ == '__main__':
    f = open("init.json", 'r')
    json_data = json.load(f)

    playerNameA = json_data['playera']
    playerNameB = json_data['playerb']
    num = int(json_data['plength'] / 2)
    fileName = json_data['file']
    nGames = json_data['ngamges']

    point_serveIn_A = np.array((1, 1) * num, dtype='uint8')
    point_serveIn_B = np.array((1, 1) * num, dtype='uint8')
    point_1st_A = np.array((0, 1) * num, dtype='uint8')
    point_1st_B = np.array((0, 1) * num, dtype='uint8')
    point_2nd_A = np.array((0, 1) * num, dtype='uint8')
    point_2nd_B = np.array((0, 1) * num, dtype='uint8')

    with codecs.open(fileName, "r", "SJIS", "ignore") as file:
        df = pd.read_table(file, delimiter=",")
    df['FirstSecond'] = df['FirstSecond'].convert_objects(
        convert_numeric=True).fillna(-1).astype(np.int)
    df = df.reset_index()

    gameLog = []
    setLog = []
    gamePoint = [0, 0]
    game = [0, 0]
    sets = [0, 0]

    pointA_array = []
    pointB_array = []

    gameA_array = []
    setA_array = []
    gameB_array = []
    setB_array = []

    flow_array = []
    point1st_array = []
    point2nd_array = []
    status = 0
    serve = 0

    for i in range(len(df)):  # len(df)
        if(df['Server'][i] == playerNameA):
            point_1st_A, point_2nd_A = calcPoint(int(df['WonA'][i]), (int(
                df['WonA'][i]) + 1) % 2, df, point_serveIn_A, point_1st_A, point_2nd_A, gamePoint)
            serve = 0
        elif(df['Server'][i] == playerNameB):
            point_1st_B, point_2nd_B = calcPoint(
                (int(
                    df['WonA'][i]) + 1) %
                2, (int(
                    df['WonA'][i]) + 1) %
                2, df, point_serveIn_B, point_1st_B, point_2nd_B, gamePoint)
            serve = 1

        if(status == 1):
            gamePoint, serve, game, status, gameLog, sets = returnTiebreakNext(
                i, gamePoint, serve, game, status, gameLog, sets)
        elif(status == 0):
            gamePoint, serve, game = returnGameNext(gamePoint, serve, game)

        game, serve, sets, status, gameLog = returnSetNext(
            i, game, serve, sets, status, gameLog)
        # status,gameWon_array,setLog=returnFinishNext(serve,sets,status,gameWon_array,setLog,3)

        per_serveIn_A = round(calcPer(point_serveIn_A), 1)
        per_serveIn_B = round(calcPer(point_serveIn_B), 1)

        per_point1st_A = round(calcPer(point_1st_A), 1)
        per_point2nd_A = round(calcPer(point_2nd_A), 1)

        per_point1st_B = round(calcPer(point_1st_B), 1)
        per_point2nd_B = round(calcPer(point_2nd_B), 1)

        pointA_array.append(gamePoint[0])
        pointB_array.append(gamePoint[1])

        gameA_array.append(game[0])
        setA_array.append(sets[0])
        gameB_array.append(game[1])
        setB_array.append(sets[1])

        flow_array.append(calcWonPer([per_serveIn_A,
                                      per_serveIn_B],
                                     [100,
                                      100],
                                     per_point1st_A,
                                     8.2,
                                     per_point2nd_A,
                                     10.8,
                                     per_point1st_B,
                                     8.2,
                                     per_point2nd_B,
                                     10.8,
                                     nGames,
                                     gamePoint,
                                     game,
                                     sets))

        point1st_array.append([per_point1st_A, per_point1st_B])
        point2nd_array.append([per_point2nd_A, per_point2nd_B])
        #print(flow_array)
    #df_add = pd.DataFrame({'PointA':pointA_array,'PointB':pointB_array,'GameA':gameA_array,'GameB':gameB_array,'SetA':setA_array,'SetB':setB_array})
    np.savetxt(fileName + '_output.csv', np.array(flow_array), delimiter=',')
    print("Complete")
