# WinProbabilitySim
This Script is for Tennis Win Probability Simulation.

You can get the win probability progress chart from point win data.

Win probability progress chart. 

![2019ausfinalosaka csv_graph](https://user-images.githubusercontent.com/7829080/52166241-14b74c00-274e-11e9-9a3e-47ded997aa24.png)


Gif Animation.

![2019ausfinalosaka csv_graph](https://user-images.githubusercontent.com/7829080/52166256-4cbe8f00-274e-11e9-84b3-29ba7b0253ad.gif)

# Input files
- **.csv

You need to prepare the csv file as below.

(Sample file "2019AusFinalOsaka.csv_output.csv")

Point by point data which won the point and which server and so on.

![screenshot](https://user-images.githubusercontent.com/7829080/52166585-85f8fe00-2752-11e9-89df-0c0db775526b.JPG)



# Output files
- Point by Point WinProbabilitiy data(.csv)
- Win probability progress chart (.png)
- Win probability progress chart Gif Animation(.gif)

# Usage
Before simulating,You need to edit the init.json


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

- "plength" This simulation is caluculated percentage of point win from last plength points.
30 points is appropriate.

When editing is completed,execute this script file
```terminal
WinProbSim.py
```
You can get Point by Point WinProbabilitiy data(.csv)

And execute this script file.
You can get Win probability progress chart (.png)
```terminal
MakeGraphPNG.py
```

And execute this script file.
You can get Win probability progress chart Gif Animation(.gif)
```terminal
MakeGraphGIF.py
```
