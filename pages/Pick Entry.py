import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_extras.switch_page_button import switch_page
import gspread 
import pandas as pd
st.set_page_config(page_title="Are You Sharper Than a Sportsbook?", layout= "wide", initial_sidebar_state="collapsed" )
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Define the scope and credentials file
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

#use to deploy
gc = gspread.service_account_from_dict(st.secrets["credentials"])
pickLog = gc.open('NFL Pick Log 2023-24')
sheets = pickLog.worksheets()
ws_names = [worksheet.title for worksheet in sheets]


#for local
#gc = gspread.service_account(filename = r"C:\Users\jmu81\NFL Picks 2023-24\Python\credentials-sheets.json")

accounts = pd.read_excel("accounts.xlsx")

accounts_users = list(accounts['Username'])




st.title("Pick Entry")
st.divider()



x = st.empty()

    




with x.form(key = "Login"):
    st.subheader("To enter and/or view picks you must enter a valid Username and Password")
    username = st.text_input(label = "Username", placeholder = None)
    password = st.text_input(label = "Password", placeholder = None , type="password")
    week_no = str(st.number_input(label="What week are you making picks for?", min_value=0, max_value=18, placeholder = None))
    submit_button = st.form_submit_button("Submit login information", use_container_width=True)
    
    
if submit_button:
    if username in (accounts_users):
        if password == st.secrets["Passwords"][username]:
            x.empty()
            with st.container():
                left, middle, right = st.columns(3)
                with left:
                    user_sheetname = "Week"+week_no+"."+username
                    week_master = pickLog.worksheet("week "+week_no+" Master")
                    user_sheet = pickLog.worksheet(user_sheetname)
                    lastrow_user = len(user_sheet.col_values(2))-1
                    st.subheader(":green[Successful login! Welcome back "+username+"!] \n Week " + week_no  + " Games")
        if user_sheetname in ws_names:
            sheet = conn.read(worksheet= user_sheetname, ttl=0, usecols = [0,1,2,3,4,5,6,9,10,11,12], nrows = lastrow_user)
            with st.container():
                st.dataframe(sheet, hide_index=True, use_container_width=True)
        else:
            sheet = pickLog.add_worksheet(title=user_sheetname)
            master_list = week_master.get_all_values()
            sheet.update("A1:Q33", master_list)
    elif password != st.secrets["Passwords"][username]:
            st.write(":red[Incorrect Username/Password. Please check for incorrect spelling.]")
    elif username not in (accounts['Username']):
        st.write(":red[Incorrect Username/Password. Please check for incorrect spelling.]")
    else:
        st.write("Please enter a Username and Password above.")

    
        

    