import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_extras.switch_page_button import switch_page
import gspread 
import toml
import os
from google.oauth2 import service_account



st.set_page_config(page_title="Are You Sharper Than a Sportsbook?", page_icon= ":red_apple:", layout= "wide", initial_sidebar_state="expanded" )

conn = st.experimental_connection("gsheets", type=GSheetsConnection)

cred_data = {
  "type": st.secrets["credentials"]["type"],
  "project_id":  st.secrets["credentials"]["project_id"],
  "private_key_id": st.secrets["credentials"]["private_key_id"],
  "private_key":  st.secrets["credentials"]["private_key"],
  "client_email":  st.secrets["credentials"]["type"],
  "client_id":  st.secrets["credentials"]["client_email"],
  "auth_uri":  st.secrets["credentials"]["auth_uri"],
  "token_uri":  st.secrets["credentials"]["token_uri"],
  "auth_provider_x509_cert_url":  st.secrets["credentials"]["auth_provider_x509_cert_url"],
  "client_x509_cert_url":  st.secrets["credentials"]["client_x509_cert_url"],
  "universe_domain":  st.secrets["credentials"]["universe_domain"]
}

# Define the scope and credentials file
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gc = service_account.Credentials.from_service_account_info(toml.loads(st.secrets["credentials"]))
#Opening the spreadsheet
pickLog = gc.open('NFL Pick Log 2023-24')
results = pickLog.worksheet("Results")
consolidated = pickLog.worksheet('Consolidated')
lastRow_consolidated = len(consolidated.col_values(1)) - 1
lastRow_Week = len(results.col_values(1)) - 1
lastRow_Season = len(results.col_values(11)) - 1  

week = conn.read(worksheet="Results", ttl = 0, usecols=[0,1,2,3,4,5,6], nrows = lastRow_Week)
season = conn.read(worksheet="Results",ttl= 0, usecols=[10,11,12,13,14,15], nrows = lastRow_Season)
st.session_state['Consolidated'] = conn.read(worksheet="Consolidated", ttl= 0, usecols =[0,1,2,3,4,5,6,7,8,9], nrows = lastRow_consolidated )
st.session_state["Users"] = season['User'].to_list()

st.title('ARE YOU _:red[SHARPER]_ THAN A SPORTSBOOK?')
st.write("##")

def reroute():
    reroute_button = st.button("Make This Weeks Picks")
    if reroute_button:
        switch_page("Pick Entry")


#Weekly Results and Season Long Results
with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        user_selection = st.selectbox(
        "What user's results do you want to see?",
        (season['User'].to_list()),
        index= None,
        placeholder ="Select user...",
        )
        st.header("Weekly Results", divider='gray')
        st.write("##")
        week_by_user = week[week.Name == user_selection]
        st.dataframe(week_by_user,
                    column_config={
                    "Weekly Winnings": st.column_config.NumberColumn(
                        format="$%d"
                    ) 
                    },
                    hide_index=True,
                    use_container_width=True
                     )
    with right_column:
        st.write("##")
        reroute()
        st.header("Season Long Leaderboard", divider="gray")
        st.write("##")
        st.dataframe(season, 
                    column_config={
                    "Overall Winnings": st.column_config.NumberColumn(
                        format="$%d"
                    ) 
                    },
                    hide_index=True,
                    use_container_width=True
                    ) 
        
