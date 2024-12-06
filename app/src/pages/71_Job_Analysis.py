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
BASE_URL = "http://api:4000/analyst" 

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

def fetch_job_ratings(company_name, job_name):
    """
    Fetch job ratings for a specific company and job, and aggregate reviews and ratings.
    """
    try:
        response = requests.get(f"{BASE_URL}/jobratings")
        response.raise_for_status()
        df = pd.DataFrame(response.json())
        
        # Filter data for the specific company and job
        filtered_df = df[(df['CompanyName'] == company_name) & (df['JobName'] == job_name)]

        if not filtered_df.empty:
            # Aggregate reviews and ratings
            aggregated_reviews = " ".join(filtered_df['Review'].tolist())
            average_rating = filtered_df['OverallRating'].mean()

            return {
                "average_rating": average_rating,
                "aggregated_reviews": aggregated_reviews,
                "detailed_ratings": filtered_df[[
                    'CompensationRating',
                    'LearningOpportunitiesRating',
                    'WorkCultureRating',
                    'WorkLifeBalanceRating'
                ]].mean().to_dict()
            }
        else:
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching job ratings: {e}")
        logger.error(f"Error fetching job ratings: {e}")
        return None


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
            if st.button(f"View Ratings for {job_name} at {company_name}", key=f"{company_id}_{job_name}"):
                ratings_data = fetch_job_ratings(company_name, job_name)

            if ratings_data:
                st.write(f"## Ratings for {company_name} - {job_name}")

                # Display the overall average rating
                st.write(f"**Average Overall Rating:** {ratings_data['average_rating']:.2f}/5")

                # Display detailed average ratings
                st.write("### Detailed Average Ratings")
                for rating_category, value in ratings_data['detailed_ratings'].items():
                    st.write(f"**{rating_category.replace('Rating', '')}:** {value:.2f}/5")

                # Display combined reviews
                st.write("### Aggregated Reviews")
                st.write(ratings_data['aggregated_reviews'])
            else:
                st.warning(f"No ratings available for {job_name} at {company_name}.")
    else:
        st.warning("No results match your search query.")
else:
    st.warning("No data available.")
