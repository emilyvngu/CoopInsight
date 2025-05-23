import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

SideBarLinks()

data = requests.get('http://api:4000/coop/jobListingDetails', data= st.session_state).json() 

id = data[0]['JobID']
name = data[0]['Name']


st.session_state['IndustryID'] = data[0]['IndustryID']
industry = requests.get('http://api:4000/coop/getIndustry', data= st.session_state).json()
industry = industry[0]['IndustryName']

st.session_state['CompanyID'] = data[0]['CompanyID']
company = requests.get('http://api:4000/coop/getCompany', data= st.session_state).json()
company = company[0]['CompanyName']

st.session_state['SkillID'] = data[0]['SkillID']
skill = requests.get('http://api:4000/coop/getSkill', data= st.session_state).json()
skill = skill[0]['SkillName']

description = data[0]['JobDescription']
minGPA = data[0]['MinGPA']
posted = data[0]['Posted']
major = data[0]['Major']

st.title(name + " Details:")
st.text("Company Name: " + company)
st.text("Industry Name: " + industry)
st.text("Required Skills: " + skill)
st.text("Desired Major: " + major)
st.text("Minimum Grade Point Average: " + str(minGPA))
st.text("Date Posted: " + posted)
st.text("Description: " + description)


maxval = requests.get('http://api:4000/coop/lastStudentID').json()[0]['StudentID']

#st.session_state['StudentID'] = st.session_state['StudentID']

if st.button("Apply to job?", type='primary', use_container_width=True):
    resp = requests.put('http://api:4000/coop/applyToJob', data= st.session_state)
    if resp.status_code == 200:
        st.text("Successfully applied to " + str(st.session_state['jobName']) + " as student: " + str(st.session_state['StudentID']) + ": " + st.session_state['username'])
    elif resp.status_code == 409:
        st.text("Already applied to job: " + str(st.session_state['jobName']) + " as student: " + str(st.session_state['StudentID']) + ": " + st.session_state['username'])
    else:
        st.text(f"Failed to apply to job: {resp.status_code}")

if st.button("Return to Job Listings", type='primary', use_container_width=True):
    st.switch_page('pages/45_User_Job_Listings_Home.py')