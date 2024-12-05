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
st.set_page_config(layout="wide", page_title="Job Ratings Dashboard")

# Display the appropriate sidebar links for the role of the logged-in user
SideBarLinks()

# Base URL for the Flask backend
BASE_URL = "http://localhost:4000/analyst"

def fetch_data(endpoint, params=None):
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()["data"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return []

# Dashboard Layout
st.title("Industry Trends Dashboard")

# Filters
time_period = st.selectbox("Time Period:", ["Last 12 Months", "Last 6 Months", "Last 3 Months"])
industry = st.selectbox("Industry:", ["All Industries", "Tech", "Healthcare", "Finance"])

# API Parameters
params = {"time_period": time_period, "industry": industry}

# Fetch and Display Data
# Average Compensation by Industry
compensation_data = fetch_data("industry_compensation", params)
if compensation_data:
    df_compensation = pd.DataFrame(compensation_data)
    st.write("### Average Compensation by Industry")
    st.bar_chart(df_compensation.set_index("Industry")["AverageCompensation"])

# Number of Available Positions
positions_data = fetch_data("available_positions", params)
if positions_data:
    st.write("### Number of Available Positions")
    st.write(f"Total Positions: {positions_data['total_positions']}")

# Top Skills in Demand
skills_data = fetch_data("top_skills", params)
if skills_data:
    st.write("### Top Skills in Demand")
    df_skills = pd.DataFrame(skills_data)
    st.bar_chart(df_skills.set_index("Skill")["Count"])

# Application Success Rate
success_rate_data = fetch_data("application_success_rate", params)
if success_rate_data:
    st.write("### Application Success Rate")
    fig, ax = plt.subplots()
    ax.pie([success_rate_data["success"], success_rate_data["failure"]],
           labels=["Success", "Failure"],
           autopct="%1.1f%%",
           startangle=90)
    ax.axis("equal")
    st.pyplot(fig)
