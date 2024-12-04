import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
import requests

SideBarLinks()

st.session_state['Position'] = st.text_input('Position: ')
position = st.session_state['Position']

dataMajors = requests.get('http://api:4000/coop/getMajors').json()

majors = pd.DataFrame(dataMajors)

major = ""

event = st.dataframe(
    majors,
    on_select='rerun',
    selection_mode='single-row'
)

if len(event.selection['rows']):
    selected_row = event.selection['rows'][0]

    st.session_state['Major'] = majors.iloc[selected_row]['Major']
    major = st.session_state['Major']

st.session_state['MinGPA'] = st.number_input('MinGPA: ', step= 0.01, min_value= 1.00, max_value= 4.00)
minGPA = st.session_state['MinGPA']

dataIndustries = requests.get('http://api:4000/coop/industry').json()

industries = pd.DataFrame(dataIndustries)

industry = ""

event = st.dataframe(
    industries,
    on_select='rerun',
    selection_mode='single-row'
)

if len(event.selection['rows']):
    selected_row = event.selection['rows'][0]

    st.session_state['IndustryID'] = industries.iloc[selected_row]['IndustryID']
    st.session_state['IndustryName'] = industries.iloc[selected_row]['IndustryName']
    industry = st.session_state['IndustryName']

st.session_state['JobDescription'] = st.text_input('Description: ')
description = st.session_state['JobDescription']

dataSkills = requests.get('http://api:4000/coop/skill').json()

skills = pd.DataFrame(dataSkills)

skill = ""

event = st.dataframe(
    skills,
    on_select='rerun',
    selection_mode='single-row'
)

if len(event.selection['rows']):
    selected_row = event.selection['rows'][0]

    st.session_state['SkillID'] = skills.iloc[selected_row]['SkillID']
    st.session_state['SkillName'] = skills.iloc[selected_row]['SkillName']
    skill = st.session_state['SkillName']

jobPosting = f'''
Position: {position}
Min GPA: {minGPA}
Major: {major}
Industry: {industry}
Description: {description}
Skill: {skill}
'''

st.text(jobPosting)

if st.button('Post job offering?', type='primary', use_container_width=True):

    requests.put('http://api:4000/coop/postJobOffer', data= st.session_state)

    st.text("Posted job offering: " + jobPosting)