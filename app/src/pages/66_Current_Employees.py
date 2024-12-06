import requests
import logging
import pandas as pd
import requests
import streamlit as st
from modules.nav import SideBarLinks

# Configure logging
logger = logging.getLogger(__name__)

# Set Streamlit page configuration
st.set_page_config(layout='wide', page_title="Employee Management Dashboard")

# Show appropriate sidebar links for the logged-in user
SideBarLinks()

# Fetch data from the API
try:
    response = requests.get('http://api:4000/coop/getEmployees', data=st.session_state)
    response.raise_for_status()
    data = response.json()
    company_name = st.session_state.get('CompanyName', "Your Company")
    df = pd.DataFrame(data)

    # Define columns to display (optional filtering)
    displayed_columns = ['EmployeeID', 'FirstName', 'LastName', 'Status', 'OfferDate', 'JobListing']
    if set(displayed_columns).issubset(df.columns):
        df = df[displayed_columns]

    # Page title
    st.title(f"👥 Current Employees for {company_name}")

    # Display the DataFrame with enhanced options
    st.markdown("### Employee List")
    with st.container():
        st.dataframe(df, use_container_width=True, height=400)
    
    if not df.empty:
        st.markdown("### Employee List")
        st.dataframe(
            df.style.format(
                formatter={
                    "OfferDate": lambda x: x.strftime("%Y-%m-%d") if not pd.isnull(x) else "",
                }
            ).highlight_max(axis=0, color="lightblue"),
            use_container_width=True,
            height=400,
        )

    # Employee selection
    st.markdown("### Actions")
    selected_employee = st.selectbox(
        "Select an employee to manage:",
        options=df.index,
        format_func=lambda idx: f"{df.loc[idx, 'FirstName']} {df.loc[idx, 'LastName']} (ID: {df.loc[idx, 'EmployeeID']})",
        index=0 if not df.empty else None,
    )

    if st.button("🛑 Terminate Employee", type='secondary'):
        if not df.empty:
            employee_id = df.loc[selected_employee, 'EmployeeID']
            st.session_state['EmployeeID'] = employee_id
            # Make API call to terminate employee
            try:
                status = requests.delete(
                    'http://api:4000/coop/terminateEmployee', data=st.session_state
                )
                if status.status_code == 200:
                    st.success(f"Employee {employee_id} has been terminated.")
                else:
                    st.error(f"Failed to terminate employee: {status.status_code}")
            except Exception as e:
                logger.error(f"Error terminating employee: {e}")
                st.error("An error occurred while terminating the employee.")
        else:
            st.warning("No employee selected. Please select an employee first.")
except requests.exceptions.RequestException as e:
    st.error("Failed to fetch employee data. Please try again later.")
    logger.error(f"Error fetching employee data: {e}")
