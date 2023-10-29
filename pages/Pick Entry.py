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

def verification(u,p):
    if u in (accounts['Username']) == True:
        if p == st.secrets["password"][u]:
            st.write(":green[Sucessful Login]")
        elif p != st.secrets["password"][u]:
            login_status = ":red[Incorrect Username/Password. Please check for incorrect spelling.]"
    elif u in (accounts['Username']) == False:
        login_status = ":red[Incorrect Username/Password. Please check for incorrect spelling.]"
    else:
        login_status = ":red[Please enter a Username and/or a Password]"

def submit_button(u,p):
    submit = st.form_submit_button("Submit login information")
    if submit:
        verification()


st.title("Pick Entry")
st.divider()

message = "To enter and/or view picks you must enter a valid Username and Password"




with st.form("Login"):
    username = st.text_input("Username", placeholder = None)
    password = st.text_input("Password", placeholder = None , type="password")
    submit = st.form_submit_button("Submit login information")
    if submit:
        verification(username,password)
    
st.subheader(message)    


