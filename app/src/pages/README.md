# `pages` Folder

The pages folder contains individual Python scripts for the various pages of your Streamlit application. Each file corresponds to a specific feature, role, or functionality in the CoopInsight platform. The folder is structured to support role-based access control (RBAC), ensuring that users only see the pages relevant to their assigned role or persona.

## Admin Pages 
- 20_Admin_Home.py: 
    - The homepage for system administrators, providing tool options.
- 21_Admin_Error_Logs.py: 
    - Displays error logs for system maintenance.
- 22_Flagged_Jobs.py & 23_Flagged_Ratings.py: 
    - Allows admins to review and address flagged job postings or ratings for quality control.

## About Page
- 30_About.py:
    - Information about our Application

## Student Pages
- 40_Users_Home.py: Serves as the homepage for all users, providing role-specific navigation and features.
- 41_User_Data.py: Displays detailed user information and provides options for viewing or editing profiles.
- 42_Skill_Data.py: Allows users to view, add, or manage skills associated with job listings or profiles.
- 43_Industry_Data.py: Displays and manages data about industries relevant to the platform.
- 44_Update_User.py: Provides functionality to update user details, including roles and permissions.
- 45_User_Job_Listings_Home.py: Acts as the main page for users to browse and filter job listings.
- 46_Detail_Job.py: Displays detailed information about a specific job listing, including requirements and company info.
- 47_Apply_To_Job.py: Enables students to submit applications for specific job postings.
- 48_Accept_Job_Offer.py: Allows users to accept job offers and updates the system accordingly.
- 49_Flag_Job_Offer.py: Enables users to flag inappropriate or suspicious job offers for admin review.
- 50_Student_Home.py: 
    - The homepage for students, showing relevant navigation options.
- 51_Coop_Dashboard.py: Displays an overview of co-op data and analytics for tracking progress and performance.
- 52_Offer_Dashboard.py: Summarizes all active offers for users, including statuses and details.

## Employer Pages
- 60_Employer_Home.py: 
    - The homepage for employers, providing options to manage job postings and view applicants.
- 61_Job_Post.py: 
    - A form for employers to post new job listings.
- 63_Applicants_Screen.py: 
    - Displays a list of applicants for a specific job, with filtering and decision-making tools.
- 64_Make_Offer.py: 
    - Allows employers to make offers to selected applicants.
- 65_Current_Offers.py: 
    - Displays and manages current job offers for students and employers, allowing actions like acceptance or rejection.
- 66_Current_Employees.py: 
    - Provides employers with a list of current employees, along with options for management or termination.
- 67_View_Job_Ratings.py: 
    - Allows users to view job ratings and reviews, offering insights into work culture, compensation, and opportunities.
- 68_Flag_Rating.py: 
    - Enables users to flag inappropriate job ratings for admin review and potential action.

## Analytics and Insights Pages 
- 70_Systems_Analyst.py: 
    - Home page for system analyst.
- 71_Job_Analysis.py: 
    - Provides insights into selected job postings with ratings.
- 72_Industry_Analysis.py: 
    - Offers industry-level analytics.
- 73_Company_Analysis.py: 
    - Displays company-level performance and feedback data.
