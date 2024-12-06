import logging
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
import requests

# Sidebar navigation
SideBarLinks()

# Title
st.title("Post a Job Offering")

# Input: Position
st.session_state['Position'] = st.text_input('Position:')
position = st.session_state.get('Position', '')

# Input: Min GPA
st.session_state['MinGPA'] = st.number_input('Minimum GPA:', step=0.01, min_value=1.00, max_value=4.00)
minGPA = st.session_state.get('MinGPA', 1.00)

# Fetch Majors
try:
    dataMajors = requests.get('http://api:4000/coop/getMajors').json()
    majors = pd.DataFrame(dataMajors)
    major_list = majors['Major'].tolist()
except Exception as e:
    st.error("Failed to load majors.")
    major_list = []

# Dropdown for Major
st.session_state['Major'] = st.selectbox(
    "Select a Major:", 
    options=["-- Enter a Major --"] + major_list, 
    index=0
)
if st.session_state['Major'] == "-- Enter a Major --":
    st.session_state['Major'] = st.text_input("Or input a major:")

# Fetch Industries
try:
    dataIndustries = requests.get('http://api:4000/coop/industry').json()
    industries = pd.DataFrame(dataIndustries)
    industry_list = industries['IndustryName'].tolist()
except Exception as e:
    st.error("Failed to load industries.")
    industry_list = []

# Dropdown for Industry
st.session_state['IndustryName'] = st.selectbox(
    "Select an Industry:", 
    options=["-- Enter an Industry --"] + industry_list, 
    index=0
)
if st.session_state['IndustryName'] == "-- Enter an Industry --":
    st.session_state['IndustryName'] = st.text_input("Or input an industry:")

# Input: Job Description
st.session_state['JobDescription'] = st.text_area('Job Description:')
description = st.session_state.get('JobDescription', '')

# Fetch Skills
try:
    dataSkills = requests.get('http://api:4000/coop/skill').json()
    skills = pd.DataFrame(dataSkills)
    skill_list = skills['SkillName'].tolist()
except Exception as e:
    st.error("Failed to load skills.")
    skill_list = []

# Dropdown for Skill
st.session_state['SkillName'] = st.selectbox(
    "Select a Skill:", 
    options=["-- Enter a Skill --"] + skill_list, 
    index=0
)
if st.session_state['SkillName'] == "-- Enter a Skill --":
    st.session_state['SkillName'] = st.text_input("Or input a skill:")

# Job Posting Preview
st.markdown("### Job Posting Preview")
jobPosting = f"""
**Position:** {position}  
**Min GPA:** {minGPA}  
**Major:** {st.session_state['Major']}  
**Industry:** {st.session_state['IndustryName']}  
**Description:** {description}  
**Skill:** {st.session_state['SkillName']}  
"""
st.markdown(jobPosting)

# Post Job Button
if st.button('Post job offering?', type='primary', use_container_width=True):
    try:
        # Send data to API
        payload = {
            "Position": st.session_state['Position'],
            "MinGPA": st.session_state['MinGPA'],
            "Major": st.session_state['Major'],
            "Industry": st.session_state['IndustryName'],
            "JobDescription": st.session_state['JobDescription'],
            "Skill": st.session_state['SkillName']
        }
        response = requests.put('http://api:4000/coop/postJobOffer', data=payload)
        
        if response.status_code == 200:
            st.success(f"Successfully posted job offering for {position}.")
        else:
            st.error(f"Failed to post job offering: {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
