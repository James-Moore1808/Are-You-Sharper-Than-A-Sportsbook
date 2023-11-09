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
                    user_sheetname = "Week"+week_no+"."+username
                    week_master = pickLog.worksheet("Week "+week_no+" Master")
                    st.subheader(":green[Successful login! Welcome back "+username+"!] \n Week " + week_no  + " Games")
        if user_sheetname in ws_names:
            user_sheet = pickLog.worksheet(user_sheetname)
            lastrow_picks = len(user_sheet.col_values(2))-1
            lastrow_scoreboard = len(user_sheet.col_values(10))-1
            sheet = conn.read(worksheet= user_sheetname, ttl=0, usecols = [0,1,2,3,4,5,6], nrows = lastrow_picks)
            scoreboard = conn.read(worksheet= user_sheetname, ttl=0, usecols = [9,10,11,12], nrows = lastrow_scoreboard)
            with st.container():
                left, right = st.columns(2)
                with left:
                    st.dataframe(sheet, hide_index=True, use_container_width=True)
                with right:
                    st.dataframe(scoreboard, hide_index=True, use_container_width=True)
        else:
            user_sheet= pickLog.add_worksheet(title=user_sheetname, rows= 50, cols= 25 )
            master_list = week_master.get_all_values()
            user_sheet.update("A1:Q33", master_list)
            lastrow_picks = len(user_sheet.col_values(2))-1
            lastrow_scoreboard = len(user_sheet.col_values(10))-1
            sheet = conn.read(worksheet= user_sheetname, ttl="60m", usecols = [0,1,2,3,4,5,6], nrows = lastrow_picks)
            scoreboard = conn.read(worksheet= user_sheetname, ttl="60m", usecols = [9,10,11,12], nrows = lastrow_scoreboard)
            scoreboard_df = pickLog.worksheet(user_sheetname)
            range1 = "J1:M"+str(lastrow_scoreboard+1)
            scoreboard_df = scoreboard_df.get(range1)
            headers = scoreboard_df.pop(0)
            scoreboard_df = pd.DataFrame(scoreboard_df, columns=headers)
            sheet['Name'] = username
            
            #The Magic
            picks = []
            st.session_state.games_col = list(sheet['Game'])
            st.session_state.away_col = list(sheet['Away'])
            st.session_state.home_col = list(sheet['Home'])

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
            #function to save the picks
            def save_picks(list):
                st.session_state['picks'].append(list)
            #fucntioon to save spreads
            def save_spreads(list):
                st.session_state['spreads'].append(list)

            #defining on click function to advance    
            def next_clicked(selection):
                if selection != st.session_state.home_col[st.session_state.counter] and selection != st.session_state.away_col[st.session_state.counter]:
                    st.write(":red[Pick a team before moving to the next selection]")
                else:
                    save_picks(game)
                    save_spreads(scoreboard_df.query(f'Team=={game}')['Spread'])
                    save_counter()


            dummy = 0
            with st.container():
                if st.session_state.counter == 0:
                    game = st.radio(
                        st.session_state.games_col[st.session_state.counter],
                        [st.session_state.home_col[st.session_state.counter], st.session_state.away_col[st.session_state.counter]],
                        captions = [scoreboard_df.query(f'Team=={st.session_state.home_col[st.session_state.counter]}')['Spread'],scoreboard_df.query(f'Team=={st.session_state.away_col[st.session_state.counter]}')['Spread']],
                    )
                    next_button = st.button("Next", on_click= next_clicked, args= game)
                else:
                    st.write(st.session_state.counter)

            
            #with st.container():
                #left, right = st.columns(2)
                #with left:
                    #st.dataframe(sheet, hide_index=True, use_container_width=True,
                                 #column_config={
                                     #"Pick": st.column_config.Column(
                                         #help = "Pick a team",
                                     #)
                                 #},
                                 #)
                #with right:
                    #st.dataframe(scoreboard, hide_index=True, use_container_width=True, disabled =['Team',"Odds", "Spread", "Opponent"])

    elif password != st.secrets["Passwords"][username]:
            st.write(":red[Incorrect Username/Password. Please check for incorrect spelling.]")
    elif username not in (accounts['Username']):
        st.write(":red[Incorrect Username/Password. Please check for incorrect spelling.]")
    else:
        st.write("Please enter a Username and Password above.")

    
        

    