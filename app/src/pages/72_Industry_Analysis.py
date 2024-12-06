import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Configure logger
logger = logging.getLogger(__name__)

# Set Streamlit page configuration
st.set_page_config(layout="wide", page_title="Industry Trends Dashboard")

# Display the appropriate sidebar links for the role of the logged-in user
SideBarLinks()

# Dashboard Layout
st.title("Industry Trends Dashboard")

# Fetch and Display Data
# Average Compensation by Industry
BASE_URL = "http://api:4000/analyst"

/industries_in_jobs
industries_list = 
time_period = st.selectbox("Select Time Period", industries_list)
industry = st.text_input("Enter Industry", "All Industries")

if st.button("Fetch Industry Compensation"):
    data = fetch_industry_compensation(time_period, industry)
    if data:
        st.write(data)
    else:
        st.error("Failed to fetch industry compensation data.")
