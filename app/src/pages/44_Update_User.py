import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
import requests

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Update Users')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

# get the countries from the world bank data
with st.echo(code_location='above'):

    minval = requests.get('http://api:4000/coop/lastUserID').json()[0]['UserID'] # this is a dictionary that im accessing the first element of and getting the value associated with the key 'UserID'

    st.session_state['UserID'] = st.number_input('UserID', min_value=minval+1, step= 1)
    st.session_state['FirstName'] = st.text_input('FirstName')
    st.session_state['LastName'] = st.text_input('LastName')
    st.session_state['Email'] = st.text_input('Email')
    st.session_state['Password'] = st.text_input('Password')
    st.session_state['PhoneNumber'] = st.text_input('PhoneNumber')

    st.text("ID: " + str(st.session_state['UserID']) + " First Name: " + st.session_state['FirstName'] + " Last Name: " + st.session_state['LastName'] + " Email: " + st.session_state['Email'] + " Password: " + st.session_state['Password'] + " Phone Number: " + st.session_state['PhoneNumber'])

if st.button('Update User Data', type='primary',use_container_width=True):
  d = {}
  for k in ('UserID', 'FirstName', 'LastName', 'Email', 'Password', 'PhoneNumber'):
     d[k] = st.session_state[k]


  requests.put('http://api:4000/coop/updateUser', data=d)
