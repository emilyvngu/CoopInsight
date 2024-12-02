import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Home, {st.session_state['username']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Apply for Co-ops',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/45_User_Job_Listings_Home.py')

if st.button('View Job Offers', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/52_Offer_Dashboard.py')