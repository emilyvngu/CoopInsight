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
st.set_page_config(layout="wide", page_title="Company Trends Dashboard")

SideBarLinks()

# Dashboard Layout
st.title("Company Trends Dashboard")

BASE_URL = "http://api:4000/analyst"

def fetch_companies():
    """
    Fetch the list of companies already in joblistings from the Flask backend.
    """
    try:
        response = requests.get(f"{BASE_URL}/companies_in_jobs") 
        response.raise_for_status() 
        return pd.DataFrame(response.json()) 
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        logger.error(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame

# Get a list of all companies names existing in joblistings
companies_list = fetch_companies()
companies_names_only = companies_list['CompanyName']

# Select widget to choose a company name
company = st.selectbox("Select Comapny", companies_names_only)

def fetch_available_positions(): 
    """
    Fetch the number of available positions for the selected Company.
    """
    try:
        response = requests.get(f"{BASE_URL}/company_available_positions")
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching available positions: {e}")
        logger.error(f"Error fetching available positions: {e}")
        return None

def fetch_skills():
    """
    Fetch all skills with its correlating company.
    """
    try:
        response = requests.get(f"{BASE_URL}/skills_with_companies")
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching available positions: {e}")
        logger.error(f"Error fetching available positions: {e}")
        return None

# Fetch Data and Populate Widgets
if st.button("Fetch Company Trends"):
    st.write(f"### Company Trends for {company}")

    # Number of Available Positions
    positions = fetch_available_positions()
    filtered_positions = positions[positions['CompanyName'] == company]
    if positions is not None:
        st.metric("Number of Available Positions", filtered_positions['JobCount'])

    # Top Skills in Demand
    top_skills = fetch_skills()

    if top_skills is not None:

        filtered_skills = top_skills[top_skills['CompanyName'] == company]
        sorted_skills = filtered_skills.sort_values(by='Demand', ascending=False)

        # Display top skills within selected company name
        if not sorted_skills.empty:
            st.write("### Top Skills in Demand")
            for _, row in sorted_skills.iterrows():
                st.write(f"- {row['SkillName']} ({row['Demand']} jobs)")
        else:
            st.write("No skills data available for the selected company.")
    else:
        st.write("No data available.")