import gspread

import pandas as pd

week_no = input("What week is it?")
wager = 10 #int(input("How much is wagered?"))


# Define the scope and credentials file
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gc = gspread.service_account(filename = r"C:\Users\jmu81\NFL Picks 2023-24\credentials-sheets.json")
#Opening the spreadsheet
pickLog = gc.open('NFL Pick Log 2023-24')

#accessing The Sheet
week = pickLog.worksheet("Week " + str(week_no) + " Master")


data = pd.read_excel(r"C:\Users\jmu81\NFL Picks 2023-24\Folder\MasterWeek"+ week_no + ".xlsx")

data['Payout'] = None


#Giving each game a payout value
for i in range(len(data)):
    odds = data['Odds'][i]
    if data['Result'][i] == 'L':
        data['Payout'][i] = -wager
    elif data['Result'][i] == 'Push':
        data['Payout'][i] = 0
    else:
        if data['Odds'][i] < 0:
            data['Payout'][i] = wager/(odds/-100)
        else:
            data['Payout'][i] = wager * (odds/100)

counter = len(data)
week.update('J1:Q33', [data.columns.tolist()] + data.values.tolist(), value_input_option='USER_ENTERED')

#Accessing the Results Column
week.update_cell(1,8,"Results")
for i in range(2,(int(counter/2)+ 2)):
    week.update_cell(i,8,"=VLOOKUP(E"+str(i)+",$J$1:Q$33,7,false)")
    week.update_cell(i,9,"=VLOOKUP(E"+str(i)+",$J$1:Q$33,8,false)")



