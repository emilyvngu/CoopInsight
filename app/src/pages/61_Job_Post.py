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

# Major Selection/Input
st.markdown("### Select or Input a Major")
try:
    dataMajors = requests.get('http://api:4000/coop/getMajors').json()
    majors = pd.DataFrame(dataMajors)
except Exception as e:
    st.error("Failed to load majors.")
    majors = pd.DataFrame()

if not majors.empty:
    st.markdown("**Available Majors:**")
    major_event = st.dataframe(majors, on_select='rerun', selection_mode='single-row', key="majors")
    if len(major_event.selection['rows']):
        selected_row = major_event.selection['rows'][0]
        st.session_state['Major'] = majors.iloc[selected_row]['Major']

# Allow user to manually input a major
st.session_state['Major'] = st.text_input("Or input a major:", value=st.session_state.get('Major', ''))

# Industry Selection/Input
st.markdown("### Select or Input an Industry")
try:
    dataIndustries = requests.get('http://api:4000/coop/industry').json()
    industries = pd.DataFrame(dataIndustries)
except Exception as e:
    st.error("Failed to load industries.")
    industries = pd.DataFrame()

if not industries.empty:
    st.markdown("**Available Industries:**")
    industry_event = st.dataframe(industries, on_select='rerun', selection_mode='single-row', key="industries")
    if len(industry_event.selection['rows']):
        selected_row = industry_event.selection['rows'][0]
        st.session_state['IndustryName'] = industries.iloc[selected_row]['IndustryName']

# Allow user to manually input an industry
st.session_state['IndustryName'] = st.text_input("Or input an industry:", value=st.session_state.get('IndustryName', ''))

# Input: Job Description
st.session_state['JobDescription'] = st.text_area('Job Description:')
description = st.session_state.get('JobDescription', '')

# Skill Selection/Input
st.markdown("### Select or Input a Skill")
try:
    dataSkills = requests.get('http://api:4000/coop/skill').json()
    skills = pd.DataFrame(dataSkills)
except Exception as e:
    st.error("Failed to load skills.")
    skills = pd.DataFrame()

if not skills.empty:
    st.markdown("**Available Skills:**")
    skill_event = st.dataframe(skills, on_select='rerun', selection_mode='single-row', key="skills")
    if len(skill_event.selection['rows']):
        selected_row = skill_event.selection['rows'][0]
        st.session_state['SkillName'] = skills.iloc[selected_row]['SkillName']

# Allow user to manually input a skill
st.session_state['SkillName'] = st.text_input("Or input a skill:", value=st.session_state.get('SkillName', ''))

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