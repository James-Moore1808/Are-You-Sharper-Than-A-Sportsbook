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

accounts_users = list(accounts['Username'])




st.title("Pick Entry")
st.subheader("To enter and/or view picks you must enter a valid Username and Password")
st.divider()


def verification(username,password):
    if username in (accounts_users):
        if password == st.secrets["Passwords"][username]:
            st.write(":green[Sucessful Login]")
        elif password != st.secrets["Passwords"][username]:
            st.write(":red[Incorrect Username/Password. Please check for incorrect spelling.]")
    elif username not in (accounts['Username']):
        st.write(":red[Incorrect Username/Password. Please check for incorrect spelling.]")
    else:
        st.write("Please enter a Username and Password above.")


with st.form(key = "Login"):
    username = st.text_input(label = "Username", placeholder = None)
    password = st.text_input(label = "Password", placeholder = None , type="password")
    submit_button = st.form_submit_button("Submit login information")
    if submit_button:
        verification(username,password)
    