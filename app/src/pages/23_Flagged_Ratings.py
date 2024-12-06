import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
import requests

SideBarLinks()

st.title("Review Flagged Ratings:")

data = requests.get('http://api:4000/admin/flaggedRatings').json()

df = pd.DataFrame(data)
if (not df.empty):
    df = df[['FlagID', 'Reason', 'UserID', 'FirstName', 'LastName', 'RatingID', 'OverallRating', 'Review', 
            'LearningOpportunitiesRating', 'CompensationRating', 'WorkCultureRating', 'WorkLifeBalanceRating']]

event = st.dataframe(
    df,
    on_select='rerun',
    selection_mode='single-row'
)

if len(event.selection['rows']):
    selected_row = event.selection['rows'][0]
    st.session_state['FlagID'] = df.iloc[selected_row]['FlagID']
    st.session_state['RatingID'] = df.iloc[selected_row]['RatingID']

    if st.button('Remove flag?', type='primary', use_container_width=True):
        status = requests.delete('http://api:4000/admin/deleteFlagRating', data=st.session_state)
        if status.status_code == 200:
            st.write(f"Flag removed!")
        else:
            st.write(f"Error: {status}")

    if st.button('Delete rating?', type='primary', use_container_width=True):
        status = requests.delete('http://api:4000/admin/deleteRating', data=st.session_state)
        if status.status_code == 200:
            st.write(f"Rating deleted!")
        else:
            st.write(f"Error: {status}")