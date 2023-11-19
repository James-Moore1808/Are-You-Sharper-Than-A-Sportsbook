import gspread
import re
import pandas as pd
import datetime




 
week_dict = dict({46:"10", 47:"11", 48:"12", 49:"13", 50:"14", 51:"15", 52:"16", 1:"17",2:"18"})
day = datetime.datetime.today()
week_no = day.isocalendar()[1]
week_no = week_dict[week_no]


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
    week = week.get(range1, value_render_option = 'FORMATTED_VALUE')
    

    if i == 1:
        #finding the index of the last row with data
        dummy2 = consolidated.col_values(1)
        last_row2 = len(dummy2) + 1
        first_row = last_row2
        range2 = "B"+str(last_row2)+":J"+str(last_row2+last_row)
        consolidated.update(range2,week, value_input_option='USER_ENTERED')
        i += 1
    else:
        last_row2 += (last_row-1)
        final_row = last_row2+last_row
        range2 = "B"+str(last_row2)+":J"+str(final_row)
        consolidated.update(range2,week, value_input_option='USER_ENTERED')
        i += 1
    counter += 1  
    
   


no_list = [[week_no]] * (final_row - first_row - 1)
range3 = "A" + str(first_row) + ":A" + str(final_row)
consolidated.update(range3, no_list, value_input_option='RAW')

