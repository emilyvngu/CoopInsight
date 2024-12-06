# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")

#### ------------------------ Examples for Role of Student (Joe Schmoe) ------------------------
def StudentHomeNav():
    st.sidebar.page_link(
        "pages/50_Student_Home.py", label="Student Home", icon="👤"
    )

def StudentJobListNav():
    st.sidebar.page_link(
        'pages/45_User_Job_Listings_Home.py', label="Job Listings", icon="🧑‍💻"
    )


def StudentOffersNav():
    st.sidebar.page_link('pages/52_Offer_Dashboard.py', label="View Offers", icon="🏙️")


#### ------------------------ Examples for Role of Employer (Jane Lane) ------------------------
def EmployerHomeNav():
    st.sidebar.page_link(
        "pages/60_Employer_Home.py", label="Employer Home", icon="👤"
    )

def JobListingsNav():
    st.sidebar.page_link("pages/62_Job_Listings.py", label="View Job Listings", icon="📋"
    )

def CurrentOffersNav():
    st.sidebar.page_link("pages/65_Current_Offers.py", label="View Current Offers", icon="🔖"
    )

def MakeOffersNav():
    st.sidebar.page_link("pages/61_Job_Post.py", label="Post An Offering", icon="🤳"
    )

def ViewEmployeesNav():
    st.sidebar.page_link(
        "pages/66_Current_Employees.py", label="View Current Employees", icon="🧑‍✈️"
    )

## ------------------------ Examples for Role of System's Analyst (Sara Lee) ------------------------
def AnalysisHomeNav():
    st.sidebar.page_link("pages/70_Systems_Analyst.py", label="Analyst HomePage", icon="👤")


def IndustryAnalysisNav():
    st.sidebar.page_link(
        "pages/72_Industry_Analysis.py", label="Industry Analysis", icon="📈"
    )


def JobAnalysisNav():
    st.sidebar.page_link(
        "pages/71_Job_Analysis.py", label="Job Analysis", icon="📊"
    )

def CompanyAnalysisNav():
    st.sidebar.page_link(
        "pages/73_Company_Analysis.py", label="Company Analysis", icon="📉"
    )


#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="👤"
)

def ErrorLogNav():
    st.sidebar.page_link("pages/21_Admin_Error_Logs.pyy", label="View Error Log", icon="🚫"
)


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("static/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # If the user role is student, show the student page
        if st.session_state["role"] == "student":
            StudentHomeNav()
            StudentJobListNav()
            StudentOffersNav()

        # If the user role is analyst, show the analyst page
        if st.session_state["role"] == "analyst":
            AnalysisHomeNav()
            JobAnalysisNav()
            CompanyAnalysisNav()
            IndustryAnalysisNav()

        # If the user is an employer, give them access to the employer pages
        if st.session_state["role"] == "employer":
            EmployerHomeNav()
            JobListingsNav()
            CurrentOffersNav()
            MakeOffersNav()
            ViewEmployeesNav()

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "debug":
            AdminPageNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
