import gspread
import re
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

user_row = len(results.col_values(11))
U_names = list(results.col_values(11))
names = U_names[1:]
exp = "Week" + week_no + "."
#getting a list of all sheets
sheets = pickLog.worksheets()
ws_names = [worksheet.title for worksheet in sheets]
ws_names = [name for name in ws_names if re.match(f"^{exp}", name)]
online_users = []
for i in range(len(ws_names)):
    dummy1  = ws_names[i].split(".")
    online_users.append(dummy1[1])
i = 0
users = len(ws_names)+1
while i < len(online_users):
    username = online_users[i]
    if username in names:
        i += 1
    else:
        user_row += 1
        results.update('K'+str(user_row), username)
        names.append(username)
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
    sheet_spec = ws_names[x]
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

