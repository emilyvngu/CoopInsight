import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

SideBarLinks()


maxval = requests.get('http://api:4000/coop/lastStudentID').json()[0]['StudentID']

st.session_state['StudentID'] = st.number_input('UserID', max_value=maxval, step= 1)

if st.button("Apply to job?", type='primary', use_container_width=True):
    requests.put('http://api:4000/coop/lastStudentID', data= st.session_state)
    st.text("Successfully applied to " + str(st.session_state['jobName']) + " as student: " + str(st.session_state['StudentID']))