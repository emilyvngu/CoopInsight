# About CoopInsight

Welcome to **CoopInsight** 

This application serves as a data-driven platform to enhance the co-op experience for Northeastern students, employers, and university administrators.

## Project Features:
- **Student Tools**: Role-specific filters, skill requirement matching, compensation ratings, and workplace culture reviews based on real student experiences.
- **Employer Tools**: Streamlined applicant filtering by skills, GPA, and major; tools for posting/editing job listings; and applicant tracking.
- **Analyst Tools**: Data insights for improving co-op opportunities, evaluating company performance, and maintaining job quality.
- **System Administration**: Tools to ensure smooth operation, including job management, user permissions, and real-time error handling.

## Meet the Team:
- **Team Name**: Databased  
- **Project Name**: CoopInsight  
- **Team Members**:
    - Andrew Cincotta (cincotta.a@northeastern.edu)  
    - Grant Petersen (petersen.g@northeastern.edu)  
    - Andrew Pluzhnikov (pluzhnikov.a@northeastern.edu)  
    - Hunter Pong (pong.h@northeastern.edu)  
    - Emily Nguyen (nguyen.emily@northeastern.edu)

## Elevator Pitch:
CoopInsight revolutionizes the co-op experience by providing detailed insights into job opportunities based on actual student data. It empowers students, employers, and university staff with tools to make informed decisions, ensuring fairness, transparency, and efficiency in the co-op search process.

The project implements a Role-Based Access Control (RBAC) system in Streamlit, allowing different features for different user roles:

## User Personas:
- **Joe Shmoe (Student)**: Navigating the co-op search process with tools to filter jobs, and rate employers.  
- **Jane Lane (Employer)**: Efficiently filtering and hiring candidates with data-backed insights.  
- **Sara Lee (Systems Analyst)**: Using data trends to optimize co-op opportunities.  
- **President Aoun (System Administrator)**: Managing database integrity, troubleshooting issues, and ensuring optimal system performance.

## Demo Video:
https://youtu.be/42vC9YdJ2BU

## Setting Up the Project with Docker
This project uses Docker to simplify the setup and deployment of its three main components: the Streamlit App, Flask API, and MySQL Database.

## Prerequisites
- docker
- docker compose 

1. Clone the Repository
2. Prepare the Environment: Navigate to the api folder and create an .env file using the provided .env.template
3. Build Containers
   ```
   docker compose build
   ```
4. Start Docker Containers
   ```
   docker compose up
   ```
6. Access the Application:
- Streamlit App: http://localhost:8501

Stay tuned for more updates and interactive features to improve the co-op experience for everyone involved!
