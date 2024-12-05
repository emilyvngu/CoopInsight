import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

name = st.session_state['username']

# Set up the base URL for the Flask backend
BASE_URL = "http://localhost:4000"  # Replace with your Flask server's URL

def fetch_job_ratings():
    """
    Fetch job ratings data from the Flask backend.
    """
    try:
        # Make a GET request to the Flask route
        response = requests.get(f"{BASE_URL}/jobratings")

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()  # Return JSON data
        else:
            st.error(f"Failed to fetch data: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

# Streamlit app layout
st.title("Job Ratings Dashboard")

# Fetch data
data = fetch_job_ratings()

# Display data if available
if data:
    st.write("### Job Ratings Data")
    for entry in data:
        st.write(entry)  # Display each entry