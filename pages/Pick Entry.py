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

u = st.empty()
p = st.empty()
sub = st.empty()
x = st.empty()

def week_selection():
    week_no = u.number_input(label="What week are you making picks for?", min_value=0, max_value=18, placeholder = None)
    submit_button_week = sub.button("Submit")
    pickLog = gc.open('NFL Pick Log 2023-24')

def verification(username,password):
    if username in (accounts_users):
        if password == st.secrets["Passwords"][username]:
            u.empty()
            p.empty()
            sub.empty()
            x.empty()
            week_selection()
            st.write("Successful login! Welcome back "+username+"!")
        elif password != st.secrets["Passwords"][username]:
            st.write(":red[Incorrect Username/Password. Please check for incorrect spelling.]")
    elif username not in (accounts['Username']):
        st.write(":red[Incorrect Username/Password. Please check for incorrect spelling.]")
    else:
        st.write("Please enter a Username and Password above.")




with x.form(key = "Login"):
    username = u.text_input(label = "Username", placeholder = None)
    password = p.text_input(label = "Password", placeholder = None , type="password")
    submit_button = sub.button("Submit login information")
    if submit_button:
        verification(username,password)
        

    