import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_extras.switch_page_button import switch_page
import gspread 
import pandas as pd

conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Define the scope and credentials file
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

#use to deploy
gc = gspread.service_account_from_dict(st.secrets["credentials"])

#for local
#gc = gspread.service_account(filename = r"C:\Users\jmu81\NFL Picks 2023-24\Python\credentials-sheets.json")

accounts = pd.read_excel("accounts.xlsx")

def verification():
    if username.isin(accounts['Username']) == True:
        if password == st.secrets[password][username]:
            login_status = ":green[Sucessful Login]"
        elif password != st.secrets[password][username]:
            login_status = ":red[Incorrect Username/Password. Please check for incorrect spelling.]"
    elif username.isin(accounts['Username']) == False:
        login_status = ":red[Incorrect Username/Password. Please check for incorrect spelling.]"
    else:
        ":red[Please enter a Username and/or a Password]"

def submit_button():
    submit = st.button("Submit login information")
    if submit_button:
        verification()


st.title("Pick Entry")
st.divider()

login_status = "To enter and/or view picks you must enter a valid Username and Password"




with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        username = st.text_input("Username", value="")
    with right_column:
        password = st.text_input("Password", value= "" , type="password")

st.subheader(login_status)
submit_button()
