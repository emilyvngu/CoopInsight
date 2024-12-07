import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

name = st.session_state['username']
st.title('System Admin Home Page')
st.write(f"Welcome, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Error Log', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Admin_Error_Logs.py')

if st.button('View Flagged Jobs', type='primary', use_container_width=True):
  st.switch_page('pages/22_Flagged_Jobs.py')

if st.button('View Flagged Ratings', type='primary', use_container_width=True):
    st.switch_page('pages/23_Flagged_Ratings.py')