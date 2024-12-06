import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Add navigation links for easy access to different app sections
SideBarLinks()

# App title and header
st.write("# CoopInsight")

# About section
st.markdown(
    """
    ## About CoopInsight

    Welcome to **CoopInsight** 
    This application serves as a data-driven platform to enhance the co-op experience for Northeastern students, employers, and university administrators.

    ### Project Features:
    - **Student Tools**: Role-specific filters, skill requirement matching, compensation ratings, and workplace culture reviews based on real student experiences.
    - **Employer Tools**: Streamlined applicant filtering by skills, GPA, and major; tools for posting/editing job listings; and applicant tracking.
    - **University Tools**: Data insights for improving co-op opportunities, evaluating company performance, and maintaining job quality.
    - **System Administration**: Tools to ensure smooth operation, including job management, user permissions, and real-time error handling.

    ### Meet the Team:
    - **Team Name**: Databased  
    - **Project Name**: CoopInsight  
    - **Team Members**:
        - Andrew Cincotta (cincotta.a@northeastern.edu)  
        - Grant Petersen (petersen.g@northeastern.edu)  
        - Andrew Pluzhnikov (pluzhnikov.a@northeastern.edu)  
        - Hunter Pong (pong.h@northeastern.edu)  
        - Emily Nguyen (nguyen.emily@northeastern.edu)

    ### Elevator Pitch:
    CoopInsight revolutionizes the co-op experience by providing detailed insights into job opportunities based on actual student data. It empowers students, employers, and university staff with tools to make informed decisions, ensuring fairness, transparency, and efficiency in the co-op search process.

    ### User Personas:
    - **Joe Shmoe (Student)**: Navigating the co-op search process with tools to filter jobs, and rate employers.  
    - **Jane Lane (Employer)**: Efficiently filtering and hiring candidates with data-backed insights.  
    - **Sara Lee (Northeastern Systems Analyst)**: Using data trends to optimize co-op opportunities.  
    - **President Aoun (System Administrator)**: Managing database integrity, troubleshooting issues, and ensuring optimal system performance.

    Stay tuned for more updates and interactive features to improve the co-op experience for everyone involved!
    """
)

st.page_link("Home.py", label="Home", icon="🏠")