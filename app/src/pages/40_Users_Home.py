import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome CoopInsight Data Viewer, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View User Data', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/41_User_Data.py')

if st.button('View Skill Data', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/42_Skill_Data.py')

if st.button('View Industry Data',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/43_Industry_Data.py')

if st.button('Update User Data', type='primary',use_container_width=True):
  st.switch_page('pages/44_Update_User.py')

if st.button('View Job Listings', type='primary',use_container_width=True):
  st.switch_page('pages/45_User_Job_Listings_Home.py')