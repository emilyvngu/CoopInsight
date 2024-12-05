import logging

import pandas as pd

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

import requests

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged-in user
SideBarLinks()

data = requests.get('http://api:4000/coop/getEmployees', data=st.session_state).json()
company_name = st.session_state['CompanyName']

df = pd.DataFrame(data)
# df = df[['OfferID', 'UserID', 'FirstName', 'LastName', 'Status', 'OfferDate', 'JobListing']]
st.title(f'Current Employees for {company_name}:')

event = st.dataframe(
    df,
    on_select='rerun',
    selection_mode='single-row'
)

if len(event.selection['rows']):
    selected_row = event.selection['rows'][0]


    if st.button("Terminate Employee", type='secondary'):
        st.session_state['EmployeeID'] = df.iloc[selected_row]['EmployeeID']
        status = requests.delete('http://api:4000/coop/terminateEmployee', data=st.session_state)
        if status.status_code == 200:
            st.write(f"Employee Terminated.")
        else:
            st.write(f"Error: {status}")
