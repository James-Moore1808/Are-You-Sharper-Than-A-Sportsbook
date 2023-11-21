import gspread
import re
import datetime
 
#ESTABLISHING WEEK NUMBERS
week_dict = dict({46:"10", 47:"11", 48:"12", 49:"13", 50:"14", 51:"15", 52:"16", 1:"17",2:"18"})
day = datetime.datetime.today()
week_no = day.isocalendar()[1]
week_no = week_dict[week_no]

# Define the scope and credentials file
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gc = gspread.service_account(filename = r"C:\Users\jmu81\Lock_It_In\Are-You-Sharper-Than-A-Sportsbook\burner-credentials.json")
#Opening the spreadsheet
pickLog = gc.open('NFL Pick Log 2023-24')
results = pickLog.worksheet("Results")

#getting a list of all possible usernames 

user_row = len(results.col_values(11))
U_names = list(results.col_values(11))
names = U_names[1:]
week_prefix = "Week" + week_no + "."
#getting a list of all sheets
sheets = pickLog.worksheets()
ws_names = [worksheet.title for worksheet in sheets]
ws_names = [name for name in ws_names if re.match(f"^{week_prefix}", name)]
online_users = []
for i in range(len(ws_names)):
    dummy1  = ws_names[i].split(".")
    online_users.append(dummy1[1])
i = 0
no_users = len(ws_names)
while i < len(online_users):
    username = online_users[i]
    if username in names:
        i += 1
    else:
        user_row += 1
        results.update('K'+str(user_row), username)
        results.update('L'+str(user_row), "=concatenate(TO_TEXT(SUMIF(B2:B1000,\"=\"&K"+ str(user_row)+",C2:C1000)),\"-\",TO_TEXT(SUMIF(B2:B1000,\"=\"&K"+ str(user_row)+",D2:D1000)),\"-\",TO_TEXT(SUMIF(B2:B1000,\"=\"&K"+ str(user_row)+",E2:E1000)))", value_input_option = "USER_ENTERED")
        results.update('M'+str(user_row), "=(SUMIF(B2:B1000,\"=\"&K"+ str(user_row)+",C2:C1000)+(0.5*(SUMIF(B2:B1000,\"=\"&K"+ str(user_row)+",E2:E1000))))/(SUMIF(B2:B1000,\"=\"&K"+ str(user_row)+",C2:C1000)+SUMIF(B2:B1000,\"=\"&K"+ str(user_row)+",D2:D1000)+SUMIF(B2:B1000,\"=\"&K"+ str(user_row)+",E2:E1000))", value_input_option = "USER_ENTERED")
        results.update('N'+str(user_row), "=(O"+ str(user_row)+")/COUNTIFS($B$2:$B$1000, \"=\"&K"+ str(user_row)+")", value_input_option = "USER_ENTERED")
        results.update('O'+str(user_row), "=COUNTIFS(Consolidated!$I$2:$I$999,\"=W\",Consolidated!$B$2:$B$999,\"=\"&K"+ str(user_row)+",Consolidated!$H$2:$H$999,\"=Y\")", value_input_option = "USER_ENTERED")
        results.update('P'+str(user_row), "=SUMIF(B:B,\"=\"&K"+ str(user_row)+",G:G)", value_input_option = "USER_ENTERED")

        
        names.append(username)
        i += 1


dummy = results.col_values(1)
first_row = len(dummy)

last_row = len(dummy) + no_users

counter = 1
x = 0
range1 = "A"+ str(first_row+1)+":A"+str(last_row)
results.update(range1, week_no)
while x < no_users:
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

