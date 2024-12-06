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

def fetch_industries():
    """
    Fetch the list of industries from the Flask backend.
    """
    try:
        response = requests.get(f"{BASE_URL}/industries_in_jobs") 
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return pd.DataFrame(response.json())  # Convert JSON to DataFrame
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        logger.error(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame

industries_list = fetch_industries()
industry = st.selectbox("Select Industry", industries_list)

if st.button("Fetch Industry Compensation"):
    data = fetch_industry_compensation(time_period, industry)
    if data:
        st.write(data)
    else:
        st.error("Failed to fetch industry compensation data.")
