import logging
logger = logging.getLogger(__name__)
import pandas as pd
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
wage = st.session_state['Wage']

st.title(name + " Details:")
st.text("Company Name: " + company)
st.text("Industry Name: " + industry)
st.text("Required Skills: " + skill)
st.text("Desired Major: " + major)
st.text("Minimum Grade Point Average: " + str(minGPA))
st.text("Date Posted: " + posted)
st.text("Description: " + description)
st.text("Wage: " + str(wage))

if st.button("Accept offer?", type='primary', use_container_width=True):
    requests.put('http://api:4000/coop/acceptOffer', data= st.session_state)
    st.text("Accepted offer for: " + name + " with wage: " + str(st.session_state['Wage']) + " as student: " + str(st.session_state['StudentID']) + ": " + st.session_state['username'])

if st.button("Reject offer?", type='primary', use_container_width=True):
    requests.put('http://api:4000/coop/rejectOffer', data= st.session_state)
    st.text("Rejected offer for: " + name + " with wage: " + str(st.session_state['Wage']) + " as student: " + str(st.session_state['StudentID']) + ": " + st.session_state['username'])
