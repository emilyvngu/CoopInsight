import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
import requests

SideBarLinks()


data = requests.get('http://api:4000/coop/getCompanyJobListings', data= st.session_state).json()

df = pd.DataFrame(data)
df = df[['JobID', 'Name', 'Major', 'MinGPA', 'SkillID', 'Posted']]
st.title('Posted Jobs Board')

event = st.dataframe(
    df,
    on_select='rerun',
    selection_mode='single-row'
)

if len(event.selection['rows']):
    selected_row = event.selection['rows'][0]
    st.session_state['JobID'] = df.iloc[selected_row]['JobID']
    st.session_state['JobName'] = df.iloc[selected_row]['Name']

    jobName = st.session_state['JobName']

    st.page_link('pages/63_Applicants_Screen.py', label=f'View {jobName} Applicants?')
    st.page_link('pages/67_View_Job_Ratings.py', label=f'View ratings for {jobName}?')