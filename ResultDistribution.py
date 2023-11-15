import gspread
import pandas as pd
import re

week_no = str(input("What week is it?"))
# Define the scope and credentials file
scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gc = gspread.service_account(filename = r"C:\Users\jmu81\NFL Picks 2023-24\credentials-sheets.json")
#Opening the spreadsheet
pickLog = gc.open('NFL Pick Log 2023-24')
results = pickLog.worksheet("Results")

#getting a list of all possible usernames 

exp = "Week" + week_no + "."
#getting a list of all sheets
sheets = pickLog.worksheets()
ws_names = [worksheet.title for worksheet in sheets]
ws_names = [name for name in ws_names if re.match(f"^{exp}", name)]


master = pickLog.worksheet("Week " + str(week_no) + " Master")
#Dataframe of Results_data to be pasted into Users' sheet
Results_table = master.get("J2:Q33")
Results_labels = master.get("J1:Q1")
results = pd.DataFrame(Results_table, columns = Results_labels)

#Dataframe of formulas to be pasted into Users' sheet
formulas_table = master.get("H2:I17", value_render_option = 'Formula')
formulas_labels = master.get("H1:I1")
formulas = pd.DataFrame(formulas_table, columns=formulas_labels)

i = 0
user_list = []
while i < len(ws_names):
    sheet_name = ws_names[i]
    week = pickLog.worksheet(sheet_name)
    week.update('H2:I17', formulas.values.tolist(), value_input_option='USER_ENTERED')
    week.update('J2:Q33', results.values.tolist(), value_input_option='RAW')
    user_list.append(sheet_name)
    i += 1


user_df = pd.DataFrame(user_list)
