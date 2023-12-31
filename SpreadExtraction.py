import pandas as pd
import requests
import datetime

Key = open('Spreads_API_Key.txt','r')
Key = Key.read()

API_Key = Key   # Key for The Odds API 

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

week_dict = dict({46:"11", 47:"12", 48:"13", 49:"14", 50:"15", 51:"16", 52:"17", 1:"18"})
today = datetime.datetime.today()
week_no = today.isocalendar()[1]

week_no = week_dict[week_no]

excel_file_path = r"C:\Users\jmu81\Lock_It_In\Are-You-Sharper-Than-A-Sportsbook\LIN_DB\SPREADSWeek"+ week_no + ".xlsx"

output.to_excel(excel_file_path, index=False)



