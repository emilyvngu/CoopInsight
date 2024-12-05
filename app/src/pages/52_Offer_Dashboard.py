import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
import requests
import time

SideBarLinks()

data = requests.get('http://api:4000/coop/studentSpecificOffers', data= st.session_state).json()

df = pd.DataFrame(data)
#df = df[['JobID', 'Wage', 'StartDate', 'EndDate', 'Status']]
df = df[['JobID', 'OfferID', 'CompanyName', 'StartDate', 'EndDate', 'Wage', 'Status']]
st.title('Offer Acceptance Board')

event = st.dataframe(
    df,
    on_select='rerun',
    selection_mode='single-row'
)

if len(event.selection['rows']):
    selected_row = event.selection['rows'][0]
    if (df.iloc[selected_row]['Status'] == 'Pending'):

        st.session_state['OfferID'] = df.iloc[selected_row]['OfferID']

        st.session_state['JobID'] = df.iloc[selected_row]['JobID']
        
        st.session_state['Wage'] = df.iloc[selected_row]['Wage']

        #st.page_link('pages/46_Detail_Job.py', label=f'Go to {jobName} Details')
        st.page_link('pages/48_Accept_Job_Offer.py', label=f'Accept this offer?')
    else:
        st.session_state['OfferID'] = df.iloc[selected_row]['OfferID']

        st.session_state['JobID'] = df.iloc[selected_row]['JobID']
        
        st.session_state['Wage'] = df.iloc[selected_row]['Wage']

        #st.page_link('pages/46_Detail_Job.py', label=f'Go to {jobName} Details')
        if st.button('Undo decision?', type='primary', use_container_width=False):
            requests.put('http://api:4000/coop/resetOffer', data= st.session_state)
            st.text("Undone decision!")
            
            time.sleep(2.5)
            st.rerun()
