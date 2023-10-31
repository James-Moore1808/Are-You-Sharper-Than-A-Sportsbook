import gspread

import pandas as pd

def is_empty(input_data):
    return len(input_data) == 0

week_no = input("What week is it?")


# Define the scope and credentials file
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gc = gspread.service_account(filename = r"C:\Users\jmu81\NFL Picks 2023-24\credentials-sheets.json")
#Opening the spreadsheet
pickLog = gc.open('NFL Pick Log 2023-24')
consolidated = pickLog.worksheet("Consolidated")
results = pickLog.worksheet("Results")

#getting a list of all possible usernames 
max_users = len(results.col_values(11))-1
users = list(results.col_values(11))
users = users[1:]

#getting a list of all sheets
sheets = pickLog.worksheets()
ws_names = [worksheet.title for worksheet in sheets]

#accessing The Sheet
counter = 0
i = 1
while counter < len(users):
    username = users[counter]
    sheet_name = "Week" + week_no + "." + username
    if sheet_name in ws_names:
        week = pickLog.worksheet(sheet_name)
        #finding the index of the last row with data
        dummy = week.col_values(4)
        last_row = len(dummy)
        range1 = "A2:I"+str(last_row)
        week = week.get(range1)
        print(week)
        

        if i == 1:
            #finding the index of the last row with data
            dummy2 = consolidated.col_values(1)
            last_row2 = len(dummy2) + 1
            range2 = "B"+str(last_row2)+":J"+str(last_row2+last_row)
            consolidated.update(range2,week)
            i += 1
        else:
            last_row2 += (last_row-1)
            range2 = "B"+str(last_row2)+":J"+str(last_row2+last_row)
            consolidated.update(range2,week)
            i += 1
        counter += 1
    else:
        counter += 1    
    
   


consolidated = pickLog.worksheet("Consolidated")
dummy = consolidated.col_values(1)
dummy2 = consolidated.col_values(6)
first_row = len(dummy)
last_row2 = len(dummy2)
for i in range((int(first_row)+1),(int(last_row2)+1)):
    consolidated.update_cell(i,1,week_no)

