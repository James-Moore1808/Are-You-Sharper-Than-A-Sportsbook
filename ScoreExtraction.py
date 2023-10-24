import requests
import pandas as pd
import json
import datetime
import openpyxl

def is_empty(input_data):
    return len(input_data) == 0


week_no = input("What week are these scores from?")


API_Key = "7f4fd734e771d78e3c5347ae5eef5a4d"   # Key for The Odds API
Date_Code = "iso"


scores_response = requests.get(
    'https://api.the-odds-api.com/v4/sports/americanfootball_nfl/scores', 
    params={
        'api_key': API_Key,
        'dateFormat': Date_Code,
        'daysFrom':3
    }
)


Results = scores_response.json()
Scoreboard = pd.DataFrame(Results)

#Removing Unnecessary Data
Scoreboard.drop(columns=['id', 'sport_key', 'sport_title'], inplace=True)
Scoreboard['commence_time'] = pd.to_datetime(Scoreboard['commence_time']).dt.date

#Setting day equal to the next wednesday
day = datetime.date.today()
while day.weekday() !=3:
    day += datetime.timedelta(1)

i = 0
x=0

#Finding the index value of the last game of the week
for i in range(len(Scoreboard)):
    if Scoreboard['commence_time'][i] < day:
        x += 1

#Cutting any games not during this week
Scoreboard = Scoreboard[0:x]

i=0
output = pd.DataFrame()
while i < len(Scoreboard):
    if is_empty(Scoreboard['scores']) == True:
        i +=1
    else:
        points = (Scoreboard['scores'][i])
        data = pd.DataFrame(points)
        i += 1
        output = pd.concat([output,data], ignore_index=True)

print(output)

day = datetime.date.today()


if day.weekday() >= 4:
    excel_file_path = r"C:\Users\jmu81\NFL Picks 2023-24\Folder\SCORESWeek"+ week_no +".xlsx"
    output.to_excel(excel_file_path, index=False)
    print(output)
else:
    scores = r"C:\Users\jmu81\NFL Picks 2023-24\Folder\SCORESWeek"+ week_no +".xlsx"
    scores = pd.read_excel(scores)
    scores = pd.concat([scores, output], ignore_index=True)
    scores = scores.drop_duplicates(subset=['name'])
    scores.to_excel(r"C:\Users\jmu81\NFL Picks 2023-24\Folder\SCORESWeek"+ week_no +".xlsx", index = False)
    print(scores)
    









