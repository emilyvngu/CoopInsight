import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
import requests

SideBarLinks()

st.session_state['Wage'] = st.number_input("Wage: ", step= 100)
st.session_state['StartDate'] = st.date_input("Start Date: ", format= 'YYYY-MM-DD')
st.session_state['EndDate'] = st.date_input("End Date: ", min_value= st.session_state['StartDate'], format= 'YYYY-MM-DD')

if st.button(label= "Make this Offer?", use_container_width=True, type='primary'):

    requests.put('http://api:4000/coop/makeOffer', data= st.session_state)

    firstName = st.session_state['FirstName']
    st.text(f"Successfully made an offer to {firstName}")