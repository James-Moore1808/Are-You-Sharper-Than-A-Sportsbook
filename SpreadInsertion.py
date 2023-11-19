import pandas as pd
pd.options.mode.chained_assignment = None
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

week_dict = dict({46:"11", 47:"12", 48:"13", 49:"14", 50:"15", 51:"16", 52:"17", 1:"18"})
today = datetime.datetime.today()
week_no = today.isocalendar()[1]

week_no = week_dict[week_no]

# Define the scope and credentials file
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\jmu81\NFL Picks 2023-24\credentials-sheets.json", scope)

# File Path to Sheet with lines 
excel_file_path = r"C:\Users\jmu81\NFL Picks 2023-24\Folder\SPREADSWeek"+ week_no +".xlsx"

# Authenticate using the credentials.
gc = gspread.authorize(credentials)

lines = pd.read_excel(excel_file_path)

#Opening the spreadsheet
pickLog = gc.open('NFL Pick Log 2023-24')
#accessing The Sheet

week = pickLog.worksheet("Week " + str(week_no) + " Master")





# Cutting cities off of the team names

i = 0
for i in range(len(lines)):
    team = lines['Team'][i]
    x = -1
    for counter in range(len(team)):
        z = team[x]
        if z == ' ':
            x += 1
            lines['Team'][i] = team[x:]
        else:
            x = x - 1

lines['Opponent'] = None

i = 0

#Adding the opponent column to the dataframe
for i in range(len(lines)):
    if i == 0:
        lines['Opponent'][i] = lines['Team'][i+1]
        i +=1
    elif lines['Team'][i] == lines['Opponent'][i-1]:
        lines['Opponent'][i] = lines['Team'][i-1]
        i += 1
    else:
        lines['Opponent'][i] = lines['Team'][i+1]
        i += 1



week.update('J1:M33', [lines.columns.tolist()] + lines.values.tolist(), value_input_option='USER_ENTERED')

lines.to_excel(r"C:\Users\jmu81\NFL Picks 2023-24\Folder\SPREADSWeek"+ week_no +".xlsx", index = False)

