import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_extras.switch_page_button import switch_page
import gspread
from streamlit_modal import Modal



st.set_page_config(page_title="Lock It In", page_icon= ":red_apple:", layout= "wide", initial_sidebar_state="expanded" )

conn = st.experimental_connection("gsheets", type=GSheetsConnection)


# Define the scope and credentials file
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

#use to deploy
gc = gspread.service_account_from_dict(st.secrets["credentials"])

#for local
#gc = gspread.service_account(filename = r"C:\Users\jmu81\NFL Picks 2023-24\Python\credentials-sheets.json")
st.session_state.home_counter = 0
app_intro = Modal(key = "Intro_modal", title = "Welcome to Lock It In!")


#Opening the spreadsheet
pickLog = gc.open("NFL Pick Log 2023-24")
results = pickLog.worksheet("Results")
consolidated = pickLog.worksheet('Consolidated')
lastRow_consolidated = len(consolidated.col_values(1)) - 1
lastRow_Week = len(results.col_values(1)) - 1
lastRow_Season = len(results.col_values(11)) - 1  

week = conn.read(worksheet="Results", ttl = 0, usecols=[0,1,2,3,4,5,6], nrows = lastRow_Week)
season = conn.read(worksheet="Results",ttl= 0, usecols=[10,11,12,13,14,15], nrows = lastRow_Season)





st.title('_:green[LOCK]_ IT IN!')
st.write("##")




#Weekly Results and Season Long Results
with st.form("Weekly Results"):
    user_selection = st.multiselect(
        "What user's results do you want to see?",
        options=(season['User'].to_list()),
        default= None,
        placeholder ="Select user...",
        )
    st.form_submit_button("Select Users", use_container_width=True)
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
        
    
if st.session_state.home_counter == 0:
    app_intro.open()
if app_intro.is_open():
    st.session_state.home_counter = 1
    with app_intro.container():
        st.write("You are currently on the Home page where you can see the season-long Leaderboard as well as weekly records. \n The Game Log page contains the records of every pick made in the 2023-24 season thus far. \n If you want to make picks you can use the sidebar to navigate to the Picks Entry tab or click the button below.")
        left,right = st.columns(2)
        with left:
            continue_button = st.button("Continue to home", use_container_width=True)
            if continue_button:
                st.session_state.home_counter = 1
                app_intro.close()
        with right:
            reroute_button = st.button("Make This Weeks Picks", use_container_width=True)
            if reroute_button:
                st.session_state.home_counter = 1
                app_intro.close()
                switch_page("Pick Entry")        
    

