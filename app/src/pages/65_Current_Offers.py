import logging

import pandas as pd

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

import requests

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged-in user
SideBarLinks()

data = requests.get('http://api:4000/coop/getCompanyOffers', data=st.session_state).json()

df = pd.DataFrame(data)
# df = df[['OfferID', 'UserID', 'FirstName', 'LastName', 'Status', 'OfferDate', 'JobListing']]
st.title(f'Current Extended Offerings:')

event = st.dataframe(
    df,
    on_select='rerun',
    selection_mode='single-row'
)

if len(event.selection['rows']):
    selected_row = event.selection['rows'][0]

    status = df.iloc[selected_row]['Status']


    if status == 'Pending' or status == 'Rejected':
        if st.button(f"{'Rescind' if status == 'Pending' else 'Delete'} Offer from Student"):
            st.session_state['OfferID'] = df.iloc[selected_row]['OfferID']
            status = requests.delete('http://api:4000/coop/withdrawOfferFromStudent', data=st.session_state)
            if status.status_code == 200:
                st.write(f"Offer withdrawn!")
            else:
                st.write(f"Error: {status}")

    if status == 'Accepted':
        st.session_state['HireID'] = df.iloc[selected_row]['UserID']
        st.session_state['JobID'] = df.iloc[selected_row]['JobID']
        st.session_state['ApplicantID'] = df.iloc[selected_row]['ApplicantID']
        st.session_state['OfferID'] = df.iloc[selected_row]['OfferID']
        if st.button("Hire Student?"):
            status = requests.post('http://api:4000/coop/hireStudent', data=st.session_state)
            if status.status_code == 200:
                st.write(f"Student hired!")
            else:
                st.write(f"Error: {status}")