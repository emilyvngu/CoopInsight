import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
import requests

# Configure logger
logger = logging.getLogger(__name__)

# Set Streamlit page configuration
st.set_page_config(layout="wide", page_title="Job Ratings Dashboard")

# Display the appropriate sidebar links for the role of the logged-in user
SideBarLinks()

# Base URL for the Flask backend
BASE_URL = "http://localhost:8501"  # Update with your Flask server URL

def fetch_companies():
    """
    Fetch the list of companies from the Flask backend.
    """
    try:
        response = requests.get(f"{BASE_URL}/companies")  # Assuming there's an endpoint for companies
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return pd.DataFrame(response.json())  # Convert JSON to DataFrame
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching companies: {e}")
        logger.error(f"Error fetching companies: {e}")
        return pd.DataFrame()  # Return an empty DataFrame

def fetch_job_ratings(company_id):
    """
    Fetch job ratings for a specific company from the Flask backend.
    """
    try:
        response = requests.get(f"{BASE_URL}/jobratings", params={"company_id": company_id})
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching job ratings: {e}")
        logger.error(f"Error fetching job ratings: {e}")
        return pd.DataFrame()

# Fetch companies
companies_df = fetch_companies()

if not companies_df.empty:
    # Select company from dropdown
    company_name = st.selectbox("Select a Company", companies_df["CompanyName"])
    selected_company_id = companies_df.loc[companies_df["CompanyName"] == company_name, "CompanyID"].values[0]

    # Fetch job ratings for the selected company
    job_ratings_df = fetch_job_ratings(selected_company_id)

    if not job_ratings_df.empty:
        # Display ratings
        st.write(f"## Ratings for {company_name}")
        for _, row in job_ratings_df.iterrows():
            st.write(f"### Job: {row['JobName']}")
            st.progress(row["OverallRating"] / 5)
            st.write(f"Work Culture: {row['WorkCultureRating']}/5")
            st.write(f"Compensation: {row['CompensationRating']}/5")
            st.write(f"Work-Life Balance: {row['WorkLifeBalanceRating']}/5")
            st.write(f"Learning Opportunities: {row['LearningOpportunitiesRating']}/5")
            st.write(f"Review: {row['Review']}")
            st.write("---")
    else:
        st.warning("No job ratings available for the selected company.")
else:
    st.warning("No companies available.")