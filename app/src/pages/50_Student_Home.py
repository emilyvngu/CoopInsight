import logging

import requests

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

maybe_employee = requests.get('http://api:4000/coop/getEmployeeInfo', data=st.session_state)
if maybe_employee.status_code == 200:
    st.session_state['EmployeeID'] = maybe_employee.json()[0]['EmployeeID']
    st.session_state['CompanyName'] = maybe_employee.json()[0]['CompanyName']
    st.session_state['CompanyID'] = maybe_employee.json()[0]['CompanyID']
    st.title(f"Welcome Home, {st.session_state['username']}.")
    st.write(f'Working for: {st.session_state["CompanyName"]}')
    st.write('')
    st.write('')
    st.write('### What would you like to do today?')
    if st.button('Resign',
                 type='secondary',
                 use_container_width=True):
        resp = requests.delete('http://api:4000/coop/resign', data=st.session_state)
        if resp.status_code == 200:
            st.write('Resignation successful.')
        else:
            st.write('Resignation failed.')
else:
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