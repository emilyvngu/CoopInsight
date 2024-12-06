import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
import requests

SideBarLinks()

data = requests.get('http://api:4000/coop/jobListings').json()

df = pd.DataFrame(data)
df = df[['JobID', 'Name', 'Major', 'MinGPA']]
st.title('Job Listings Board')

event = st.dataframe(
    df,
    on_select='rerun',
    selection_mode='single-row'
)

if len(event.selection['rows']):
    selected_row = event.selection['rows'][0]

    st.session_state['JobID'] = df.iloc[selected_row]['JobID']

    jobName = df.iloc[selected_row]['Name']

    st.session_state['jobName'] = jobName

    #st.page_link('pages/46_Detail_Job.py', label=f'Go to {jobName} Details')
    st.page_link('pages/47_Apply_To_Job.py', label=f'Apply to {jobName}')
    st.page_link('pages/49_Flag_Job_Offer.py', label=f'Flag {jobName} for administrator review?')

if st.button('Go Home', type='secondary'):
    st.switch_page('pages/50_Student_Home.py')