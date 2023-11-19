import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_extras.switch_page_button import switch_page
import gspread
from streamlit_modal import Modal
import numpy as np


st.set_page_config(page_title="Lock It In", layout= "wide", initial_sidebar_state="auto" )

conn = st.experimental_connection("gsheets", type=GSheetsConnection)


# Define the scope and credentials file
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

#use to deploy
gc = gspread.service_account_from_dict(st.secrets["credentials"])

#for local
#gc = gspread.service_account(filename = r"C:\Users\jmu81\NFL Picks 2023-24\Python\credentials-sheets.json")



#Opening the spreadsheet and making necessary connections between google sheets and streamlit
pickLog = gc.open("NFL Pick Log 2023-24")
results = pickLog.worksheet("Results")
consolidated = pickLog.worksheet('Consolidated')
lastRow_consolidated = len(consolidated.col_values(1)) - 1
lastRow_Week = len(results.col_values(1)) - 1
lastRow_Season = len(results.col_values(11)) - 1 
week = conn.read(worksheet="Results", ttl = 10, usecols=[0,1,2,3,4,5,6], nrows = lastRow_Week)
season = conn.read(worksheet="Results",ttl= 10, usecols=[10,11,12,13,14,15], nrows = lastRow_Season)
valid_Week_Nos = np.array(week['Week'].to_list())
valid_Week_Nos = np.unique(valid_Week_Nos)
valid_users = np.array(season['User'].to_list())
valid_users = np.unique(valid_users)

#Button to reroute to picks entry
def reroute(input):
    reroute_button = st.button(label= "Make This Weeks Picks", key=str(input))
    if reroute_button:
        switch_page("Pick Entry")


# Title configuration
image_col, title_col = st.columns([.05,.80])
with image_col:
    st.caption("")
    st.image("https://cdn.dribbble.com/users/3735278/screenshots/9876390/media/a59d044e0ebc39dc295e1c5726236f85.gif", width=80)
with title_col:
    st.title('LOCK IT IN!')

#Making the Tabs
st.write("This app allows you to make picks against the spread and track your performance for the 2023-24 NFL Season")
tabWeeklyLeaderboard, tabSeasonLongLeaderboard, tabAbout = st.tabs(["Weekly Leaderboard", "Season Long Leaderboard", "About"])

#Filling in The Weekly Leaderboard tab
with tabWeeklyLeaderboard:
    with st.form("Weekly Results"):
        left, right = st.columns(2)
        with left:
            user_selection = st.multiselect(
                "What user's results do you want to see?",
                options=(valid_users),
                default= valid_users[:],
                )
        with right:
            week_selection = st.multiselect(
               "What user's results do you want to see?",
                options=(valid_Week_Nos),
                default= valid_Week_Nos[-1:],
            )
        st.form_submit_button("Select User(s) and Week(s)", use_container_width=True)
        st.header("Weekly Results", divider='gray')
        st.write("##")
        week_by_user = week[week['Name'].isin(user_selection)]
        filtered_week = week[week['Week'].isin(week_selection)]
        st.dataframe(filtered_week,
                    column_config={
                    "Weekly Winnings": st.column_config.NumberColumn(
                        format="$%.2f",
                        help="If a user were to put $10 on each game (since week 8) this would be their net gain/loss week-by-week"
                    ) ,
                    'Win %': st.column_config.NumberColumn(
                        format="%.3f"
                    )
                    },
                    hide_index=True,
                    use_container_width=True
                        )
    reroute(1)
            

# Filling in the Season Long Leaderboard tab
with tabSeasonLongLeaderboard:
    st.header("Season Long Leaderboard", divider="gray")
    st.write("##")
    st.dataframe(season, 
                column_config={
                "Overall Winnings": st.column_config.NumberColumn(
                    format="$%.2f",
                    help="If a user were to put $10 on each game (since week 8) this would be their net gain/loss"
                ),
                'Win %': st.column_config.NumberColumn(
                    format="%.3f"
                ),
                'Lock Efficiency': st.column_config.NumberColumn(
                    format="%.3f"
                )
                },
                hide_index=True,
                use_container_width=True
                ) 
    



# Filling in the About tab

with tabAbout:
    st.write("Weclome to ***Lock It In!***")
    st.markdown("""
                You are currently on the Home page where you can access each users weekly record
                in addition to the Season Long Leaderbaord. 

                If you want to see the breakdown of the exact picks for a user for a specific week 
                or group of weeks use the sidebar to navigate to the ***Game Logs*** page.

                If you want to make picks please use the sidebar to navigate to the Pick Entry page
                or click the button below ⤵️
                """)
    reroute(2)