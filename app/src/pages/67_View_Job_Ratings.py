import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
import requests

SideBarLinks()

data = requests.get('http://api:4000/coop/getJobRatings', data= st.session_state).json()

jobName = st.session_state['JobName']

df = pd.DataFrame(data)
if (not df.empty):
    df = df[['RatingID', 'OverallRating', 'Review', 'CompensationRating', 'LearningOpportunitiesRating', 'WorkCultureRating', 'WorkLifeBalanceRating']]
st.title(f'{jobName} Ratings:')

event = st.dataframe(
    df,
    on_select='rerun',
    selection_mode='single-row'
)

if len(event.selection['rows']):
    selected_row = event.selection['rows'][0]
    st.session_state['RatingID'] = df.iloc[selected_row]['RatingID']
    
    st.page_link('pages/68_Flag_Rating.py', label='Flag this rating for administrator review?')