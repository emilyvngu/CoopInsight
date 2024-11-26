import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
import requests

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('World Bank Data')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

# get the countries from the world bank data
with st.echo(code_location='above'):
    results = requests.get('http://api:4000/coop/skill').json()
    print(results)
    st.dataframe(results)