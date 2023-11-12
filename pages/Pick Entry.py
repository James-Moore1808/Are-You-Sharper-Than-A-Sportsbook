import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_extras.switch_page_button import switch_page
import gspread 
import pandas as pd
import time
st.set_page_config(page_title="Are You Sharper Than a Sportsbook?", layout= "wide", initial_sidebar_state="collapsed" )
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Define the scope and credentials file
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

#use to deploy
gc = gspread.service_account_from_dict(st.secrets["pick_entry_credentials"])
pickLog = gc.open('NFL Pick Log 2023-24')
sheets = pickLog.worksheets()
ws_names = [worksheet.title for worksheet in sheets]


#for local
#gc = gspread.service_account(filename = r"C:\Users\jmu81\NFL Picks 2023-24\Python\pickentry_credentials.json")

accounts = pd.read_excel("accounts.xlsx")

accounts_users = list(accounts['Username'])




st.title("Pick Entry")
st.divider()



x = st.empty()
rd = st.empty()    


#initializing the picks list - LOGGING IN COUNTER
if "account_counter" not in st.session_state:
    st.session_state.account_counter = 0

#LOGGING IN
if st.session_state.account_counter == 0:
    with x.form(key = "Login"):
        st.subheader("To enter and/or view picks you must enter a valid Username and Password")
        username = st.text_input(label = "Username", placeholder = None)
        password = st.text_input(label = "Password", placeholder = None , type="password")
        week_no = str(st.number_input(label="What week are you making picks for?", min_value=0, max_value=18, placeholder = ""))
        submit_button = st.form_submit_button("Submit login information", use_container_width=True)
    if submit_button:
        if username in (accounts_users):
            if password == st.secrets["Passwords"][username]:
                x.empty()
                with st.container():
                    left, middle, right = st.columns(3)
                    with left:
                        st.session_state.username = username
                        st.session_state.week_no = week_no
                        st.subheader(":green[Successful login! Welcome back "+username+"!] \n Week " + week_no  + " Games")
                st.session_state.user_sheetname = "Week"+week_no+"."+username
                #SETTING THE SHEET THAT WILL BE SHOWN NEXT
                if st.session_state.user_sheetname in ws_names:
                    st.session_state.dummy_counter = 0
                else:
                    st.session_state.dummy_counter = 1
                #HIDING THIS LOGGING IN BLOCK OF CODE
                st.session_state.account_counter = 1
        elif password != st.secrets["Passwords"][username]:
                st.write(":red[Incorrect Username/Password. Please check for incorrect spelling.]")
        elif username not in (accounts['Username']):
            st.write(":red[Incorrect Username/Password. Please check for incorrect spelling.]")
        else:
            st.write("Please enter a Username and Password above.")
    


    
#RESULTS IN SHEET CREATION OR SHOWING THE CURRENT PICKS SHEET    
if st.session_state.account_counter == 1:
    if st.session_state.dummy_counter == 0:
        user_sheet = pickLog.worksheet(st.session_state.user_sheetname)
        lastrow_picks = len(user_sheet.col_values(2))-1
        lastrow_scoreboard = len(user_sheet.col_values(10))-1
        sheet = conn.read(worksheet= st.session_state.user_sheetname, ttl=0, usecols = [0,1,2,3,4,5,6], nrows = lastrow_picks)
        scoreboard = conn.read(worksheet= st.session_state.user_sheetname, ttl=0, usecols = [9,10,11,12], nrows = lastrow_scoreboard)
        with st.container():
            left, right = st.columns(2)
            with left:
                st.dataframe(sheet, hide_index=True, use_container_width=True)
            with right:
                st.dataframe(scoreboard, hide_index=True, use_container_width=True)
    elif st.session_state.dummy_counter == 1:
        user_sheet= pickLog.add_worksheet(title=st.session_state.user_sheetname, rows= 50, cols= 25 )
        week_master = pickLog.worksheet("Week "+st.session_state.week_no+" Master")
        master_list = week_master.get_all_values()
        user_sheet.update("A1:Q33", master_list)
        st.session_state.lastrow_picks = len(user_sheet.col_values(2))
        st.session_state.lastrow_scoreboard = len(user_sheet.col_values(10))
        st.session_state.dummy_counter = 2
        st.session_state.account_counter = 2
        
        master_df = pickLog.worksheet(st.session_state.user_sheetname)
        picks_range = "A1:G"+str(st.session_state.lastrow_picks) 
        scoreboard_range = "J1:M"+str(st.session_state.lastrow_scoreboard)
        picks_df = master_df.get(picks_range)
        scoreboard_df = master_df.get(scoreboard_range)
        picks_headers = picks_df.pop(0)
        scoreboard_headers = scoreboard_df.pop(0)
        picks_df = pd.DataFrame(picks_df, columns=picks_headers)
        st.session_state.picks_df = picks_df
        scoreboard_df = pd.DataFrame(scoreboard_df, columns=scoreboard_headers)
        st.session_state.scoreboard_df = scoreboard_df


#PICK SELECTION BLOCK
if st.session_state.account_counter == 2:
    picks_df = st.session_state.picks_df
    scoreboard_df = st.session_state.scoreboard_df
    picks_df['Name'] = st.session_state.username

    
    #THE MAGIC
    picks = []
    st.session_state.games_col = list(picks_df['Game'])
    st.session_state.away_col = list(picks_df['Away'])
    st.session_state.home_col = list(picks_df['Home'])

    #initializing a session state counter
    if "counter" not in st.session_state:
        st.session_state.counter = 0

    #initializing the picks list
    if "picks" not in st.session_state:
        st.session_state.picks = []

    #initializing the picks list
    if "spreads" not in st.session_state:
        st.session_state.spreads = []


    #function to save the counter
    def save_counter():
        st.session_state.counter += 1
    #function to decrease the counter
    def dec_counter():
        st.session_state.counter -= 1

    #function to save the picks
    def save_picks(list):
        st.session_state['picks'].append(list)
    #fucntioon to save spreads
    def save_spreads(list):
        st.session_state['spreads'].append(list)


    def submit_clicked():
        st.write(game)

    if st.session_state.counter == 0:
        i = 0
        with st.form("pick_selection"):
            for i in range(0,(st.session_state.lastrow_picks-1)):
                team_list = [st.session_state.home_col[i], st.session_state.away_col[i]]
                game = st.radio(
                    st.session_state.games_col[i],
                    team_list,
                    captions = [scoreboard_df.query(f"Team=='{team_list[0]}'")['Spread'].to_list()[0],scoreboard_df.query(f"Team=='{team_list[1]}'")['Spread'].to_list()[0]],
                    index=None
                )
                st.session_state['picks'].append(game)
            submit_button = st.form_submit_button(label = "Submit!", use_container_width=True, on_click=submit_clicked)

    


#DATAFRAME DISPLAY AND LOCK SELECTION
if st.session_state.account_counter == 3:
    picks_df = st.session_state.picks_df
    picks_df['Name'] = st.session_state.username
    picks_df['Pick'] = st.session_state.picks
    picks_df['Pick Spread'] = st.session_state.spreads
    with rd.form("final"):
        df = st.data_editor(picks_df, hide_index=True, use_container_width=True,
                        column_config={
                            "Lock?": st.column_config.SelectboxColumn(
                            help="Pick Y for whatever game you feel best about. Choose wisely!",
                            options=[
                                "N",
                                "Y"
                                     ],
                            required=True
                            ),
                            "Name":st.column_config.Column(disabled=True, required=True),
                            "Game":st.column_config.Column(disabled=True, required=True),
                            "Away":st.column_config.Column(disabled=True, required=True),
                            "Home":st.column_config.Column(disabled=True, required=True),
                            "Pick":st.column_config.Column(disabled=True, required=True),
                            "Pick Spread":st.column_config.Column(disabled=True, required=True)
                        })
        final_submit = st.form_submit_button(label="Lock in picks!", use_container_width=True)
        if final_submit:
            count = df["Lock?"].value_counts().get("Y", 0)
            if count > 1:
                st.subheader(":warning: :red[TOO MANY LOCKS] :warning:")
            elif count == 0:
                st.subheader(":red[Please select a lock]")
            elif count == 1:
                week = pickLog.worksheet(st.session_state.user_sheetname)
                week.update("A1:G"+str(st.session_state.lastrow_picks), [df.columns.tolist()] + df.values.tolist(), value_input_option='USER_ENTERED' )
                rd.empty()
                st.session_state.account_counter = 4        



if st.session_state.account_counter == 4:
    st.subheader("Picks have been entered, best of luck!")
    user_sheet = pickLog.worksheet(st.session_state.user_sheetname)
    lastrow_picks = len(user_sheet.col_values(2))-1
    lastrow_scoreboard = len(user_sheet.col_values(10))-1
    sheet = conn.read(worksheet= st.session_state.user_sheetname, ttl=0, usecols = [0,1,2,3,4,5,6], nrows = lastrow_picks)
    scoreboard = conn.read(worksheet= st.session_state.user_sheetname, ttl=0, usecols = [9,10,11,12], nrows = lastrow_scoreboard)
    with st.container():
        left, right = st.columns(2)
        with left:
            st.dataframe(sheet, hide_index=True, use_container_width=True)
        with right:
            st.dataframe(scoreboard, hide_index=True, use_container_width=True)

                



            

    