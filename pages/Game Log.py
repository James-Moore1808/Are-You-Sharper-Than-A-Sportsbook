import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_extras.switch_page_button import switch_page
import gspread 
import pandas as pd

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
gc = gspread.service_account_from_dict(st.secrets["credentials"])
st.title("Game Log")
st.divider()


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
                "Weekly Winnings": st.column_config.NumberColumn(
                format="$%d"
                ) 
                },
                hide_index=True,
                use_container_width=True
                )
