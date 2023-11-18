import streamlit as st
from streamlit_gsheets import GSheetsConnection
import gspread


st.set_page_config(page_title="Game Log", layout= "wide", initial_sidebar_state="collapsed" )
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Define the scope and credentials file
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

#use to deploy
gc = gspread.service_account_from_dict(st.secrets["credentials"])
pickLog = gc.open("NFL Pick Log 2023-24")
consolidated = pickLog.worksheet('Consolidated')
lastRow_consolidated = len(consolidated.col_values(1)) - 1

#for local
#gc = gspread.service_account(filename = r"C:\Users\jmu81\NFL Picks 2023-24\Python\credentials-sheets.json")

st.session_state['Consolidated'] = conn.read(worksheet="Consolidated", ttl= 0, usecols =[0,1,2,3,4,5,6,7,8,9], nrows = lastRow_consolidated )
st.title("Game Log")
st.divider()

with st.form("Game Log"):
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            user_selection = st.multiselect(
                "Which user(s) results are you interested in seeing?",
                options=st.session_state["Users"],
                default=None,
                placeholder="Select user(s)...",
            )
        with right_column:
            week_selection = st.multiselect(
                'Which week(s) are you interested in seeing?',
                options = list(range(1,19)),
                default = None,
                placeholder="Select Week(s)"
            )

    consolidated = st.session_state["Consolidated"]
    with st.container():
        dummy = consolidated[consolidated['Week'].isin(week_selection)]
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
