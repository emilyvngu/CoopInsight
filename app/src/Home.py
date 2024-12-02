##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout='wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page.
logger.info("Loading the Home page of the app")
st.title('CoopInsight')

# NEU logo image sample
st.write('\n')
#st.image("static/logo.png", caption="NEU logo")
st.markdown("[![Northeastern Website](app/static/logo.png)](https://www.northeastern.edu/)")

# simple prompt
st.write('\n\n')
st.write('### Which persona would you like to demo?')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

if st.button("Act as Joe Shmoe, a Student currently on search for a Co-op.",
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'student'
    st.session_state['username'] = 'Joe Shmoe'
    st.session_state['UserID'] = 1
    st.session_state['StudentID'] = 51

    logger.info("Logging in as Student Persona; Joe Shmoe.")
    st.switch_page('pages/50_Student_Home.py')

if st.button('Act as Jane Lane, an Employer looking to hire a Co-op.',
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'employer'
    st.session_state['username'] = 'Jane Lane'

    st.switch_page('pages/60_Employer_Home.py')

if st.button('Act as Sara Lee, our System\'s Analyst.',
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'analyst'
    st.session_state['username'] = 'Sara Lee'

    st.switch_page('pages/70_Systems_Analyst.py')

if st.button('Act as Aoun, our System\'s Admin.',
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'debug'
    st.session_state['username'] = 'SysAdmin'

    st.switch_page('pages/20_Admin_Home.py')

st.write("Copyright® 2024 Databsed, Inc. All rights reserved.")  # :)
