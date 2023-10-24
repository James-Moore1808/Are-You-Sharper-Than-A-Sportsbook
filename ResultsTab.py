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
results = pickLog.worksheet("Results")

dummy = results.col_values(1)
first_row = len(dummy)
print(first_row)
last_row = len(dummy) + users
print(last_row)
counter = 1
range1 = "A"+ str(first_row+1)+":A"+str(last_row)
results.update(range1, week_no)
while counter <= users:
    week = pickLog.worksheet("Week " + str(week_no) + "." + str(counter))
    name =week.get('A2') 
    
    results.update_cell(first_row+counter,1, week_no)
    results.update_cell(first_row+counter,2,name[0][0])
    results.update_cell(first_row+counter,3, "=COUNTIFS(Consolidated!$B$2:$B$999,\"=\"&$B" +str(first_row+counter)+",Consolidated!$I$2:$I$999,\"=W\",Consolidated!$A$2:$A$999,\"=\"&$A" +str(first_row+counter)+")")
    results.update_cell(first_row+counter,4, "=COUNTIFS(Consolidated!$B$2:$B$999,\"=\"&$B" +str(first_row+counter)+",Consolidated!$I$2:$I$999,\"=L\",Consolidated!$A$2:$A$999,\"=\"&$A" +str(first_row+counter)+")")
    results.update_cell(first_row+counter,5, "=COUNTIFS(Consolidated!$B$2:$B$999,\"=\"&$B" +str(first_row+counter)+",Consolidated!$I$2:$I$999,\"=Push\",Consolidated!$A$2:$A$999,\"=\"&$A" +str(first_row+counter)+")")
    results.update_cell(first_row+counter,6, "=SUM(C" +str(first_row+counter)+",(E" +str(first_row+counter)+"*0.5))/SUM(C" +str(first_row+counter)+":E" +str(first_row+counter)+")")
    results.update_cell(first_row+counter,7, "=SUMIFS(Consolidated!J:J,Consolidated!A:A,\"=\"&$A"+str(first_row+counter)+",Consolidated!B:B,\"=\"&$B"+str(first_row+counter)+")")
    counter += 1
