import gspread

import pandas as pd

def is_empty(input_data):
    return len(input_data) == 0

week_no = input("What week is it?")
users = int(input("How many users gave picks?"))

# Define the scope and credentials file
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gc = gspread.service_account(filename = r"C:\Users\jmu81\NFL Picks 2023-24\credentials-sheets.json")
#Opening the spreadsheet
pickLog = gc.open('NFL Pick Log 2023-24')
consolidated = pickLog.worksheet("Consolidated")

#accessing The Sheet
counter = 1
while counter <= users:
    week = pickLog.worksheet("Week " + str(week_no) + "." + str(counter))
    #finding the index of the last row with data
    dummy = week.col_values(4)
    last_row = len(dummy)
    range1 = "A2:I"+str(last_row)
    week = week.get(range1)
    print(week)
    

    if counter == 1:
        #finding the index of the last row with data
        dummy2 = consolidated.col_values(1)
        last_row2 = len(dummy2) + 1
        range2 = "B"+str(last_row2)+":J"+str(last_row2+last_row)
        consolidated.update(range2,week)
        i = 1
    else:
        last_row2 += (last_row-1)
        range2 = "B"+str(last_row2)+":J"+str(last_row2+last_row)
        consolidated.update(range2,week)
        
    
    counter += 1


consolidated = pickLog.worksheet("Consolidated")
dummy = consolidated.col_values(1)
dummy2 = consolidated.col_values(6)
first_row = len(dummy)
last_row2 = len(dummy2)
for i in range((int(first_row)),(int(last_row2)+1)):
    consolidated.update_cell(i,1,week_no)

