import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

BASE_URL = "http://api:4000/admin"

def fetch_error_logs():
    """
    Fetch error logs from the API.
    """
    response = requests.get(f"{BASE_URL}/error_logs")
    response.raise_for_status()
    return pd.DataFrame(response.json())

# Page: Track Error Logs
st.title("Track Error Logs")

# Fetch and display error logs
error_logs_df = fetch_error_logs()
if not error_logs_df.empty:
    st.write("### Error Logs")
    st.dataframe(error_logs_df)
else:
    st.write("No error logs available.")
