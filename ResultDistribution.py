import gspread

import pandas as pd

week_no = input("What week is it?")
users = int(input("How many users?"))

# Define the scope and credentials file
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gc = gspread.service_account(filename = r"C:\Users\jmu81\NFL Picks 2023-24\credentials-sheets.json")
#Opening the spreadsheet
pickLog = gc.open('NFL Pick Log 2023-24')
master = pickLog.worksheet("Week " + str(week_no) + " Master")

#Dataframe of Results_data to be pasted into Users' sheet
Results_table = master.get("J2:Q33")
Results_labels = master.get("J1:Q1")
results = pd.DataFrame(Results_table, columns = Results_labels)

formulas_table = master.get("H2:I17", value_render_option = 'Formula')
formulas_labels = master.get("H1:I1")
formulas = pd.DataFrame(formulas_table, columns=formulas_labels)

counter = 1
while counter <= users:
    week = pickLog.worksheet("Week " + str(week_no) + "." + str(counter))
    week.update('H2:I17', formulas.values.tolist(), value_input_option='USER_ENTERED')
    week.update('J2:Q33', results.values.tolist(), value_input_option='USER_ENTERED')
    counter += 1