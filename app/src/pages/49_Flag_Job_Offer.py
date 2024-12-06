import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

SideBarLinks()

jobName = st.session_state['jobName']

st.title(f"Flagging {jobName} for administrator review:")

reason = st.text_input("Reason for flag: ")
st.session_state['Reason'] = reason

if st.button('Flag for review?', type='primary', use_container_width=True):
    status = requests.post('http://api:4000/coop/flagJob', data=st.session_state)
    if status.status_code == 200:
        st.write(f"Job flagged for review!")
    else:
        st.write(f"Error: {status}")