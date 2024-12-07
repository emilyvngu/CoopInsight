import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

name = st.session_state['username']
st.title('Systems Analyst Dashboard')
st.write(f"Welcome, {name}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Analyze Jobs', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/71_Job_Analysis.py')

if st.button('Analyze Companies', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/73_Company_Analysis.py')

if st.button('Analyze Industries', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/72_Industry_Analysis.py')