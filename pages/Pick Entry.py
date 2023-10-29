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






st.title("Pick Entry")
st.divider()

message = "To enter and/or view picks you must enter a valid Username and Password"

def verification():
    if username in (accounts['Username']) == True:
        if password == st.secrets["password"][username]:
            st.write(":green[Sucessful Login]")
        elif password != st.secrets["password"][username]:
            st.write(":red[Incorrect Username/Password. Please check for incorrect spelling.]")
    elif username in (accounts['Username']) == False:
        st.write(":red[Incorrect Username/Password. Please check for incorrect spelling.]")
    else:
        st.write(":red[Please enter a Username and/or a Password]")


with st.form("Login"):
    username = st.text_input("Username", placeholder = None)
    password = st.text_input("Password", placeholder = None , type="password")
    submit = st.form_submit_button("Submit login information", on_click = verification, args = None)
    
    
st.subheader(message)    


