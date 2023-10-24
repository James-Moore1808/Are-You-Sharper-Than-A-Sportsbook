import pandas as pd
import requests
import json
import openpyxl
import datetime

API_Key = "7f4fd734e771d78e3c5347ae5eef5a4d"   # Key for The Odds API

Sport_key = "americanfootball_nfl"

Regions = "us"

Markets = "spreads"

Date_Code = "iso"

Odds_format = "american"

Bookmaker = 'fanduel'


day = datetime.date.today()
if day.weekday() > 3:
    while day.weekday() !=3:
        day += datetime.timedelta(1)
else:
    day += datetime.timedelta(7)


sports_response = requests.get(
    'https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds', 
    params={
        'api_key': API_Key,
        'regions': Regions,
        'markets': Markets,
        'oddsFormat': Odds_format,
        'dateFormat': Date_Code,
        'bookmakers': Bookmaker,
        'commenceTimeTo': str(day)+"T12:00:00Z"

    }
)


GameLines = sports_response.json()
print(GameLines)
week = pd.DataFrame(GameLines)


i = 0
output = pd.DataFrame()
while i < len(week):
    game = (week['bookmakers'][i])
    data = (game[0]['markets'][0]['outcomes'])
    spreads = pd.DataFrame(data)
    spreads.rename(columns={'name': 'Team', 'price': 'Odds', 'point': 'Spread'}, inplace=True)
    i +=1
    output = pd.concat([output,spreads], ignore_index=True)

print(output)

week_no = input("What week is it?")

excel_file_path = r"C:\Users\jmu81\NFL Picks 2023-24\Folder\SPREADSWeek"+ week_no + ".xlsx"

output.to_excel(excel_file_path, index=False)



