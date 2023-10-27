import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_extras.switch_page_button import switch_page
import gspread 
import pandas as pd

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
gc = gspread.service_account_from_dict(st.secrets["credentials"])

st.write("What are yoiu doing in this mf")
