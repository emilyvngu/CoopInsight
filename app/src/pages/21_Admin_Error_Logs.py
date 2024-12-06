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
    response = requests.get(f"{BASE_URL}/error_logs")
    return response.json()

if st.button("Fetch Error Logs"):
    logs = fetch_error_logs()
    st.write(pd.DataFrame(logs))
