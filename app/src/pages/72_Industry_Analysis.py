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
        response.raise_for_status() 
        return pd.DataFrame(response.json())  # Convert JSON to DataFrame
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        logger.error(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame

industries_list = fetch_industries()
industries_names_only = industries_list['IndustryName']
industry = st.selectbox("Select Industry", industries_names_only)

def fetch_available_positions():
    """
    Fetch the number of available positions for the selected industry.
    """
    try:
        response = requests.get(f"{BASE_URL}/available_positions")
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching available positions: {e}")
        logger.error(f"Error fetching available positions: {e}")
        return None

# Fetch Data and Populate Widgets
if st.button("Fetch Industry Trends"):
    st.write(f"### Industry Trends for {industry}")

    # Number of Available Positions
    positions = fetch_available_positions()
    filtered_positions = positions[positions['IndustryName'] == industry]
    if positions is not None:
        st.metric("Number of Available Positions", positions)

    # Top Skills in Demand
    top_skills = fetch_top_skills(industry)
    if top_skills:
        st.write("### Top Skills in Demand")
        for skill in top_skills:
            st.write(f"- {skill['SkillName']} ({skill['Demand']} jobs)")

    # Application Success Rate
    success_rate = fetch_application_success_rate(industry)
    if success_rate is not None:
        st.metric("Application Success Rate", f"{success_rate:.2f}%")
