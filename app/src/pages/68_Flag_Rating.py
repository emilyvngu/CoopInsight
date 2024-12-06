import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

SideBarLinks()

ratingID = st.session_state['RatingID']

st.title(f"Flagging {ratingID} for administrator review:")

reason = st.text_input("Reason for flag: ")
st.session_state['Reason'] = reason

if st.button('Flag for review?', type='primary', use_container_width=True):
    status = requests.post('http://api:4000/coop/flagRating', data=st.session_state)
    if status.status_code == 200:
        st.write(f"Rating flagged for review!")
    else:
        st.write(f"Error: {status}")