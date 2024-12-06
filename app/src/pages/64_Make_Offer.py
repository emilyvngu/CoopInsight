import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
import requests

# Sidebar links
SideBarLinks()

# Page title
st.title("Post an Offering")

# Input fields for the job offering
st.session_state['Position'] = st.text_input("Position:", placeholder="Enter the job title")
st.session_state['MinGPA'] = st.number_input("Minimum GPA:", min_value=1.0, max_value=4.0, step=0.1, value=1.0)
st.session_state['Major'] = st.text_input("Major:", placeholder="Enter the required major")
st.session_state['Industry'] = st.text_input("Industry:", placeholder="Enter the industry")
st.session_state['Description'] = st.text_area("Description:", placeholder="Enter a detailed job description")
st.session_state['Skill'] = st.text_input("Skill:", placeholder="Enter required skills")

# Input fields for wage and dates
st.session_state['Wage'] = st.number_input("Wage:", step=100, min_value=0)
st.session_state['StartDate'] = st.date_input("Start Date:")
st.session_state['EndDate'] = st.date_input("End Date:", min_value=st.session_state['StartDate'])

# Submit button
if st.button(label="Post this Offering", type='primary', use_container_width=True):
    try:
        # Prepare the data to send
        offering_data = {
            "Position": st.session_state['Position'],
            "MinGPA": st.session_state['MinGPA'],
            "Major": st.session_state['Major'],
            "IndustryID": st.session_state.get('IndustryID', None),  # Use an ID for backend compatibility if needed
            "JobDescription": st.session_state['Description'],
            "SkillID": st.session_state.get('SkillID', None),  # Use an ID for backend compatibility if needed
            "Wage": st.session_state['Wage'],
            "StartDate": st.session_state['StartDate'].strftime("%Y-%m-%d"),
            "EndDate": st.session_state['EndDate'].strftime("%Y-%m-%d"),
        }

        # API call to post the offering
        response = requests.put('http://api:4000/coop/postJobOffer', data=offering_data)
        
        if response.status_code == 200:
            st.success(f"Successfully posted the offering: {st.session_state['Position']}")
        else:
            st.error(f"Failed to post the offering. Error: {response.text}")
    
    except Exception as e:
        logger.error(f"Error posting offering: {e}")
        st.error("An unexpected error occurred while posting the offering.")
