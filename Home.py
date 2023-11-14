import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_extras.switch_page_button import switch_page
import gspread




st.set_page_config(page_title="Are You Sharper Than a Sportsbook?", page_icon= ":red_apple:", layout= "wide", initial_sidebar_state="collapsed" )

conn = st.experimental_connection("gsheets", type=GSheetsConnection)


# Define the scope and credentials file
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

#use to deploy
gc = gspread.service_account_from_dict(st.secrets["credentials"])

#for local
#gc = gspread.service_account(filename = r"C:\Users\jmu81\NFL Picks 2023-24\Python\credentials-sheets.json")

#Opening the spreadsheet
pickLog = gc.open("NFL Pick Log 2023-24")
results = pickLog.worksheet("Results")
consolidated = pickLog.worksheet('Consolidated')
lastRow_consolidated = len(consolidated.col_values(1)) - 1
lastRow_Week = len(results.col_values(1)) - 1
lastRow_Season = len(results.col_values(11)) - 1  

week = conn.read(worksheet="Results", ttl = 0, usecols=[0,1,2,3,4,5,6], nrows = lastRow_Week)
season = conn.read(worksheet="Results",ttl= 0, usecols=[10,11,12,13,14,15], nrows = lastRow_Season)
st.session_state['Consolidated'] = conn.read(worksheet="Consolidated", ttl= 0, usecols =[0,1,2,3,4,5,6,7,8,9], nrows = lastRow_consolidated )
st.session_state["Users"] = season['User'].to_list()

def reroute():
    reroute_button = st.button("Make This Weeks Picks")
    if reroute_button:
        switch_page("Pick Entry")



st.title('ARE YOU _:red[SHARPER]_ THAN A SPORTSBOOK?')
st.write("##")




#Weekly Results and Season Long Results
with st.form("Weekly Results"):
    user_selection = st.multiselect(
        "What user's results do you want to see?",
        options=(season['User'].to_list()),
        default= None,
        placeholder ="Select user...",
        )
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("Weekly Results", divider='gray')
        st.write("##")
        week_by_user = week[week['Name'].isin(user_selection)]
        st.dataframe(week_by_user,
                    column_config={
                    "Weekly Winnings": st.column_config.NumberColumn(
                        format="$%d",
                        help="If a user were to put $10 on each game \n (since week 8) this would be their net gain/loss week-by-week"
                    ) 
                    },
                    hide_index=True,
                    use_container_width=True
                     )
    with right_column:
        st.header("Season Long Leaderboard", divider="gray")
        st.write("##")
        st.dataframe(season, 
                    column_config={
                    "Overall Winnings": st.column_config.NumberColumn(
                        format="$%d",
                        help="If a user were to put $10 on each game \n (since week 8) this would be their net gain/loss"
                    ) 
                    },
                    hide_index=True,
                    use_container_width=True
                    ) 
    st.form_submit_button("Select Users", use_container_width=True)
    
reroute()    
    
        
    

