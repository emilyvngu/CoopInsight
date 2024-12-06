import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
import requests

SideBarLinks()

st.title("Review Flagged Jobs:")

data = requests.get('http://api:4000/admin/flaggedJobs').json()

df = pd.DataFrame(data)
if (not df.empty):
    df = df[['FlagID', 'Reason', 'JobID', 'CompanyName', 'JobName']]

event = st.dataframe(
    df,
    on_select='rerun',
    selection_mode='single-row'
)

if len(event.selection['rows']):
    selected_row = event.selection['rows'][0]
    st.session_state['FlagID'] = df.iloc[selected_row]['FlagID']
    st.session_state['JobID'] = df.iloc[selected_row]['JobID']

    if st.button('Remove flag?', type='primary', use_container_width=True):
        status = requests.delete('http://api:4000/admin/deleteFlagJob', data=st.session_state)
        if status.status_code == 200:
            st.write(f"Flag removed!")
        else:
            st.write(f"Error: {status}")

    if st.button('Delete job?', type='primary', use_container_width=True):
        status = requests.delete('http://api:4000/admin/deleteJob', data=st.session_state)
        if status.status_code == 200:
            st.write(f"Job deleted!")
        else:
            st.write(f"Error: {status}")