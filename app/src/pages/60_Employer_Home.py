import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

name = st.session_state['username']
st.session_state['CompanyID'] = requests.get('http://api:4000/coop/getCompanyID', data=st.session_state).json()[0]['CompanyID']
companyID = st.session_state['CompanyID']
st.title('Employer Home')
st.write(f"Welcome, {name}, ID: {companyID}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Job Listings', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/62_Job_Listings.py')

if st.button('View World Map Demo', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Map_Demo.py')