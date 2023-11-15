import gspread
import re
import pandas as pd

def is_empty(input_data):
    return len(input_data) == 0

week_no = str(input("What week is it?"))


# Define the scope and credentials file
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gc = gspread.service_account(filename = r"C:\Users\jmu81\NFL Picks 2023-24\credentials-sheets.json")
#Opening the spreadsheet
pickLog = gc.open('NFL Pick Log 2023-24')
consolidated = pickLog.worksheet("Consolidated")
results = pickLog.worksheet("Results")

#getting a list of all possible usernames 

exp = "Week" + week_no + "."
#getting a list of all sheets
sheets = pickLog.worksheets()
ws_names = [worksheet.title for worksheet in sheets]
ws_names = [name for name in ws_names if re.match(f"^{exp}", name)]
#accessing The Sheet
counter = 0
i = 1
while counter < len(ws_names):
    sheet_name = ws_names[counter]
    week = pickLog.worksheet(sheet_name)
    #finding the index of the last row with data
    dummy = week.col_values(4)
    last_row = len(dummy)
    range1 = "A2:I"+str(last_row)
    week = week.get(range1)
    

    if i == 1:
        #finding the index of the last row with data
        dummy2 = consolidated.col_values(1)
        last_row2 = len(dummy2) + 1
        first_row = last_row2
        range2 = "B"+str(last_row2)+":J"+str(last_row2+last_row)
        consolidated.update(range2,week, value_input_option='RAW')
        i += 1
    else:
        last_row2 += (last_row-1)
        final_row = last_row2+last_row
        range2 = "B"+str(last_row2)+":J"+str(final_row)
        consolidated.update(range2,week, value_input_option='RAW')
        i += 1
    counter += 1  
    
   


range3 = list(range(first_row,(final_row+1)))
for i in range(0,(final_row-first_row+1)):
    consolidated.update("A"+str(range3[i]), week_no , value_input_option='user_entered')