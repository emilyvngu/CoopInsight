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

# Base URL for the Flask backend
BASE_URL = "http://api:4000/analyst"

# Dashboard Layout
st.title("Industry Trends Dashboard")

# Fetch and Display Data
# Average Compensation by Industry
BASE_URL = "http://api:4000/analyst"

def fetch_industry_compensation(time_period, industry):
    """
    Fetch the industry compensation data from the API.
    """
    try:
        # Construct the URL with dynamic parameters
        url = f"{BASE_URL}/industry_compensation/{time_period}/{industry}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching industry compensation: {e}")
        return None

time_period = st.selectbox("Select Time Period", ["All Time", "Last 12 Months", "Last 6 Months"])
industry = st.text_input("Enter Industry", "All Industries")

if st.button("Fetch Industry Compensation"):
    data = fetch_industry_compensation(time_period, industry)
    if data:
        st.write(data)
    else:
        st.error("Failed to fetch industry compensation data.")
