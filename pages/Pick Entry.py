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

#for local
#gc = gspread.service_account(filename = r"C:\Users\jmu81\NFL Picks 2023-24\Python\credentials-sheets.json")

accounts = pd.read_excel("accounts.xlsx")

accounts_users = list(accounts['Username'])




st.title("Pick Entry")
st.divider()



x = st.empty()

    

def verification(username,password):
    if username in (accounts_users):
        if password == st.secrets["Passwords"][username]:
            x.empty()
            with st.container:
                left, middle, right = st.columns = 2
                with left:
                    st.subheader(":green[Successful login! Welcome back "+username+"!]")
                with middle:
                    st.subheader("Picks for Week" + week_no)
        elif password != st.secrets["Passwords"][username]:
            st.subheader(":red[Incorrect Username/Password. Please check for incorrect spelling.]")
    elif username not in (accounts['Username']):
        st.subheader(":red[Incorrect Username/Password. Please check for incorrect spelling.]")
    else:
        st.subheader("Please enter a Username and Password above.")




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
                left, middle, right = st.columns(2)
                with left:
                    st.subheader(":green[Successful login! Welcome back "+username+"!]")
                with middle:
                    st.subheader("Picks for Week " + week_no)  
        elif password != st.secrets["Passwords"][username]:
            st.write(":red[Incorrect Username/Password. Please check for incorrect spelling.]")
    elif username not in (accounts['Username']):
        st.write(":red[Incorrect Username/Password. Please check for incorrect spelling.]")
    else:
        st.write("Please enter a Username and Password above.")

    
        

    