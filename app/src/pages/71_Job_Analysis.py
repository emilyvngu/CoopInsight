import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

# Configure logger
logger = logging.getLogger(__name__)

# Set Streamlit page configuration
st.set_page_config(layout="wide", page_title="Job Ratings Dashboard")

# Display the appropriate sidebar links for the role of the logged-in user
SideBarLinks()

# Base URL for the Flask backend
BASE_URL = "http://localhost:8501" 

def fetch_companies_and_jobs():
    """
    Fetch the list of companies and jobs from the Flask backend.
    """
    try:
        response = requests.get(f"{BASE_URL}/companies_jobs")  # Assuming an endpoint that returns companies and jobs
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return pd.DataFrame(response.json())  # Convert JSON to DataFrame
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        logger.error(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame

def fetch_job_ratings(company_id):
    """
    Fetch job ratings for a specific company from the Flask backend.
    """
    try:
        response = requests.get(f"{BASE_URL}/jobratings")
        response.raise_for_status()
        df = pd.DataFrame(response.json())
        return df[df['company_id'] = company_id]
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching job ratings: {e}")
        logger.error(f"Error fetching job ratings: {e}")
        return pd.DataFrame()

# Fetch companies and jobs data
companies_jobs_df = fetch_companies_and_jobs()

if not companies_jobs_df.empty:
    # Search bar for companies or jobs
    search_query = st.text_input("Search for a company or job", "").lower()

    # Filter companies and jobs based on search query
    filtered_df = companies_jobs_df[
        companies_jobs_df["CompanyName"].str.lower().str.contains(search_query) |
        companies_jobs_df["JobName"].str.lower().str.contains(search_query)
    ]

    if not filtered_df.empty:
        st.write("### Search Results")
        for _, row in filtered_df.iterrows():
            company_id = row["CompanyID"]
            company_name = row["CompanyName"]
            job_name = row["JobName"]

            st.write(f"**Company:** {company_name}")
            st.write(f"**Job:** {job_name}")
            
            # Button to fetch ratings for the selected company
            if st.button(f"View Ratings for {job_name} at {company_name}", key=company_id):
                ratings_df = fetch_job_ratings()

                if not ratings_df.empty:
                    st.write(f"## Ratings for {company_name} - {job_name}")
                    for _, rating_row in ratings_df.iterrows():
                        st.write(f"### Job: {rating_row['JobName']}")
                        st.progress(rating_row["OverallRating"] / 5)
                        st.write(f"Work Culture: {rating_row['WorkCultureRating']}/5")
                        st.write(f"Compensation: {rating_row['CompensationRating']}/5")
                        st.write(f"Work-Life Balance: {rating_row['WorkLifeBalanceRating']}/5")
                        st.write(f"Learning Opportunities: {rating_row['LearningOpportunitiesRating']}/5")
                        st.write(f"Review: {rating_row['Review']}")
                        st.write("---")
                else:
                    st.warning(f"No ratings available for {job_name} at {company_name}.")
    else:
        st.warning("No results match your search query.")
else:
    st.warning("No data available.")
