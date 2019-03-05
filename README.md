# TennisWinProbSim
![2019ausfinalosaka csv_graph](https://user-images.githubusercontent.com/7829080/52166241-14b74c00-274e-11e9-9a3e-47ded997aa24.png)

TennisWinProbSim is python programs for simulate win probability in tennis match.
For python3.xx.

Monte Carlo simulation by random number calculation.

You can get the win probability fluctuation chart from point won data.

# Demo
GIF Animation.

![2019ausfinalosaka csv_graph](https://user-images.githubusercontent.com/7829080/52166256-4cbe8f00-274e-11e9-84b3-29ba7b0253ad.gif)

# Input files
- csvfile

If you want to calculate the simulation,you need to prepare the csv file as below.

(Sample file "2019AusFinalOsaka.csv_output.csv")

Point by point won data which won the point and which server and so on.

![screenshot](https://user-images.githubusercontent.com/7829080/52166585-85f8fe00-2752-11e9-89df-0c0db775526b.JPG)

In row of FirstSecond,you edit the 1 or 2.
At that point,if 1st serve was in,you edit the 1,
Else if 1st serve was fault,you edit the 2.

In row of Set,you edit set as that point.
In row of Server,At that point,which the serve is.
In row of WonA,If playerA got the point,you edit 1.
If not,you edit 0.

# Output files
If you calc the simulation,you obtain this files.
- Point by Point WinProbabilitiy data(.csv)
- Win probability progress chart (.png)
- Win probability progress chart Gif Animation(.gif)

# Dependency
- python3
- pandas
- numpy
- matplotlib
- sys
- json

# Usage
1. Clone this repository to your working directory.

2. Before simulating,You need to edit the init.json

```json
{
	"file":"2019AusFinalOsaka.csv",
	"firstsecond":0,
	"playera":"Osaka",
	"playerb":"Kvitova",
	"set1":"7-6",
	"set2":"5-7",
	"set3":"6-4",
	"plength":30,
	"ngamges":1000
	}
```
- "file" Rewrite the filename of csvfile that is windata point by point

- "firstsecond" 0:ignore serve 1st2nd 1:serve 1st2nd

- "playera" "playerb" Rewrite the playerName a and b.This name is needed to match

- "plength" This simulation is caluculated percentage of point win from last plength points.
30 points is default.

- "ngames" Number of caluculations.1000 is recommended.

3. When editing is completed,open this ipynb file on the JupyterNotebook.
```terminal
WinProbSim.ipynb
```
If you execute the top script,you can get Point by Point WinProbabilitiy data(.csv)

4. And if execute the second script,you can get Win probability progress chart (.png)

5. If execute the third script,you can get Win probability progress chart Gif Animation(.gif)

# Related Site
[【試合の流れの可視化】勝率推移シミュレーション、データ集計から勝率チャート作成まで自動出力できるようにしました](http://datatennis.net/archives/5042/)

# Licence
This software is released under the MIT License, see LICENSE.
