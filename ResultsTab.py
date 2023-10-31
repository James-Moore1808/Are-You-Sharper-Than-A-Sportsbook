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
results = pickLog.worksheet("Results")

#getting a list of all possible usernames 
max_users = len(results.col_values(11))-1
names = list(results.col_values(11))
names = names[1:]

#getting a list of all sheets
sheets = pickLog.worksheets()
ws_names = [worksheet.title for worksheet in sheets]

i = 0
users = 0
users_list = []
while i < len(names):
    username = names[i]
    sheet_name = "Week" + week_no + "." + username
    if sheet_name in ws_names:
        users += 1
        users_list.append(sheet_name)
        i += 1
    else:
        i += 1

dummy = results.col_values(1)
first_row = len(dummy)
print(first_row)
last_row = len(dummy) + users
print(last_row)
counter = 1
x = 0
range1 = "A"+ str(first_row+1)+":A"+str(last_row)
results.update(range1, week_no)
while x < users:
    sheet_spec = users_list[x]
    week = pickLog.worksheet(sheet_spec)
    name =week.get('A2') 
    
    results.update_cell(first_row+counter,1, week_no)
    results.update_cell(first_row+counter,2,name[0][0])
    results.update_cell(first_row+counter,3, "=COUNTIFS(Consolidated!$B:$B,\"=\"&$B" +str(first_row+counter)+",Consolidated!$I:$I,\"=W\",Consolidated!$A:$A,\"=\"&$A" +str(first_row+counter)+")")
    results.update_cell(first_row+counter,4, "=COUNTIFS(Consolidated!$B:$B,\"=\"&$B" +str(first_row+counter)+",Consolidated!$I:$I,\"=L\",Consolidated!$A:$A,\"=\"&$A" +str(first_row+counter)+")")
    results.update_cell(first_row+counter,5, "=COUNTIFS(Consolidated!$B:$B,\"=\"&$B" +str(first_row+counter)+",Consolidated!$I:$I,\"=Push\",Consolidated!$A:$A,\"=\"&$A" +str(first_row+counter)+")")
    results.update_cell(first_row+counter,6, "=SUM(C" +str(first_row+counter)+",(E" +str(first_row+counter)+"*0.5))/SUM(C" +str(first_row+counter)+":E" +str(first_row+counter)+")")
    results.update_cell(first_row+counter,7, "=SUMIFS(Consolidated!J:J,Consolidated!A:A,\"=\"&$A"+str(first_row+counter)+",Consolidated!B:B,\"=\"&$B"+str(first_row+counter)+")")
    counter += 1
    x += 1
