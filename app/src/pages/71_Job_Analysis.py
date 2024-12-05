import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

# Select company
conn = create_connection()
company_df = pd.read_sql("SELECT CompanyID, CompanyName FROM Company", conn)
conn.close()

company_id = st.selectbox("Select a Company", company_df["CompanyName"])
selected_company_id = company_df.loc[company_df["CompanyName"] == company_id, "CompanyID"].values[0]

# Display ratings
ratings_df = get_job_ratings(selected_company_id)
st.write(f"## Ratings for {company_id}")
for index, row in ratings_df.iterrows():
    st.write(f"### Job: {row['JobName']}")
    st.progress(row["OverallRating"] / 5)
    st.write(f"Work Culture: {row['WorkCultureRating']}/5")
    st.write(f"Compensation: {row['CompensationRating']}/5")
    st.write(f"Work-Life Balance: {row['WorkLifeBalanceRating']}/5")
    st.write(f"Learning Opportunities: {row['LearningOpportunitiesRating']}/5")
    st.write(f"Review: {row['Review']}")
    st.write("---")