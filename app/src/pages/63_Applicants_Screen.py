import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
import requests

SideBarLinks()

dataApplicants = requests.get('http://api:4000/coop/getCompanyJobApplicants', data= st.session_state).json()

dfApplicants = pd.DataFrame(dataApplicants)

jobName = st.session_state['JobName']

st.title(f'Applicants to {jobName}:')

event = st.dataframe(
    dfApplicants,
    on_select='rerun',
    selection_mode='single-row'
)

if len(event.selection['rows']):
    selected_row = event.selection['rows'][0]

    st.session_state['ApplicantID'] = dfApplicants.iloc[selected_row]['ApplicantID']
    st.session_state['JobID'] = dfApplicants.iloc[selected_row]['JobID']
    st.session_state['StudentID'] = dfApplicants.iloc[selected_row]['StudentID']

    dataStudent = requests.get('http://api:4000/coop/getApplicantProfile', data= st.session_state).json()

    st.session_state['UserID'] = dataStudent[0]['UserID']

    dataUser = requests.get('http://api:4000/coop/getStudentUserDetails', data= st.session_state).json()

    st.text("Name: " + dataUser[0]['FirstName'] + " " + dataUser[0]['LastName'])
    st.text("Email: " + dataUser[0]['Email'])
    st.text("GPA: " + str(dataStudent[0]['GPA']))
    st.text("Major: " + dataStudent[0]['Major'])

    st.session_state['SkillID'] = dataStudent[0]['Skill']

    dataSkill = requests.get('http://api:4000/coop/getSkill', data= st.session_state).json()

    st.text("Skill: " + dataSkill[0]['SkillName'])

    firstName = dataUser[0]['FirstName']
    st.session_state['FirstName'] = firstName
    st.session_state['ApplicantID'] = st.session_state['StudentID']

    st.page_link('pages/64_Make_Offer.py', label=f'Make a job offer to {firstName}?')