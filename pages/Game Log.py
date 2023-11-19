import streamlit as st
from streamlit_gsheets import GSheetsConnection
import gspread
import numpy as np

st.set_page_config(page_title="Game Log", layout= "wide", initial_sidebar_state="collapsed" )
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Define the scope and credentials file
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

#use to deploy
gc = gspread.service_account_from_dict(st.secrets["credentials"])
pickLog = gc.open("NFL Pick Log 2023-24")
results = pickLog.worksheet("Results")
consolidated = pickLog.worksheet('Consolidated')
lastRow_consolidated = len(consolidated.col_values(1)) - 1
lastRow_Week = len(results.col_values(1)) - 1
lastRow_Season = len(results.col_values(11)) - 1 
week = conn.read(worksheet="Results", ttl = 0, usecols=[0,1,2,3,4,5,6], nrows = lastRow_Week)
season = conn.read(worksheet="Results",ttl= 0, usecols=[10,11,12,13,14,15], nrows = lastRow_Season)
valid_Week_Nos = np.array(week['Week'].to_list())
valid_Week_Nos = np.unique(valid_Week_Nos)
valid_users = np.array(season['User'].to_list())
valid_users = np.unique(valid_users)

#for local
#gc = gspread.service_account(filename = r"C:\Users\jmu81\NFL Picks 2023-24\Python\credentials-sheets.json")

games = conn.read(worksheet="Consolidated", ttl= 0, usecols =[0,1,2,3,4,5,6,7,8,9], nrows = lastRow_consolidated )

st.title("Game Log")
st.divider()

with st.form("Game Log"):
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
           user_selection = st.multiselect(
                "What user's results do you want to see?",
                options=(valid_users),
                default= valid_users[:],
                )
        with right_column:
           week_selection = st.multiselect(
               "What user's results do you want to see?",
                options=(valid_Week_Nos),
                default= valid_Week_Nos[-1:],
            )
    with st.container():
        dummy = games[games['Week'].isin(week_selection)]
        log = dummy[dummy['Name'].isin(user_selection)]
        st.dataframe(log,
                    column_config={
                    "Payout": st.column_config.NumberColumn(
                    format="$%d",
                    help = "If a user were to put 10 dollars on each game (since week 8) \nthis would be their game-by-game net gain/loss"
                    ) 
                    },
                    hide_index=True,
                    use_container_width=True
                    )
    st.form_submit_button("Select Users", use_container_width=True)
