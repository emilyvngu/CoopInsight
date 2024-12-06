########################################################
# Analyst blueprint of endpoints
########################################################
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
import sys
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Create a new Blueprint object
analyst = Blueprint('analyst', __name__)


#------------------------------------------------------------
# Get all jobratings info
@analyst.route('/jobratings', methods=['GET'])
def get_job_ratings():
    try:
        cursor = db.get_db().cursor()
        query = """
            SELECT c.CompanyName, j.Name AS JobName, r.OverallRating, r.WorkCultureRating,
                r.CompensationRating, r.WorkLifeBalanceRating, r.LearningOpportunitiesRating, r.Review
            FROM Rating r
            JOIN JobListing j ON r.JobID = j.JobID
            JOIN Company c ON r.CompanyID = c.CompanyID
        """
        cursor.execute(query)

        theData = cursor.fetchall()

        the_response = make_response(jsonify(theData))
        the_response.status_code = 200
        return the_response
    
    except Exception as e:
        # Log the error and return a 500 response
        logger.error(f"Error fetching job ratings: {e}")
        return make_response(jsonify({"error": "An error occurred while fetching job ratings."}))


#------------------------------------------------------------
# Get all jobs and companies

@analyst.route('/companies_jobs', methods=['GET'])
def get_companies_and_jobs():
    try:
        # Get a database cursor
        cursor = db.get_db().cursor()

        # Query to fetch companies and their jobs
        query = """
            SELECT c.CompanyID, c.CompanyName, j.Name AS JobName
            FROM Company c
            JOIN JobListing j ON c.CompanyID = j.CompanyID
            ORDER BY c.CompanyName, j.Name
        """
        cursor.execute(query)

        # Fetch results
        theData = cursor.fetchall()

        the_response = make_response(jsonify(theData))
        the_response.status_code = 200
        return the_response
    
    except Exception as e:
        # Log the error and return a 500 response
        logger.error(f"Error fetching jobs: {e}")
        return make_response(jsonify({"error": "An error occurred while fetching jobs."}))

#------------------------------------------------------------
# Get all industries already in job listings
@analyst.route('/industries_in_jobs', methods=['GET'])
def get_industries_in_jobs():
    try:
        cursor = db.get_db().cursor()

        # Query to fetch industries with job listings
        query = """
            SELECT DISTINCT i.IndustryID, i.IndustryName
            FROM Industry i
            JOIN JobListing j ON i.IndustryID = j.IndustryID
            ORDER BY i.IndustryName
        """
        cursor.execute(query)

        theData = cursor.fetchall()

        response = make_response(jsonify(theData))
        response.status_code = 200
        return response

    except Exception as e:
        print(f"Error fetching industries in jobs: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@analyst.route('/available_positions/<industry>', methods=['GET'])
def get_available_positions(industry):
    try:
        cursor = db.get_db().cursor()

        # Query to fetch the number of available positions
        query = """
            SELECT COUNT(j.JobID) AS AvailablePositions
            FROM JobListing j
            JOIN Industry i ON j.IndustryID = i.IndustryID
        """
        params = []

        if industry != "All Industries":
            query += " WHERE i.IndustryName = %s"
            params.append(industry)

        cursor.execute(query, params)
        result = cursor.fetchone()

        # Return the data as JSON
        return jsonify({"AvailablePositions": result[0]}), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching available positions: {e}")
        return jsonify({"error": str(e)}), 500

@analyst.route('/top_skills/<industry>', methods=['GET'])
def get_top_skills(industry):
    try:
        cursor = db.get_db().cursor()

        # Query to fetch the most required skills
        query = """
            SELECT s.SkillName, COUNT(js.SkillID) AS Demand
            FROM JobSkill js
            JOIN Skill s ON js.SkillID = s.SkillID
            JOIN JobListing j ON js.JobID = j.JobID
            JOIN Industry i ON j.IndustryID = i.IndustryID
        """
        params = []

        if industry != "All Industries":
            query += " WHERE i.IndustryName = %s"
            params.append(industry)

        query += " GROUP BY s.SkillName ORDER BY Demand DESC LIMIT 10"

        cursor.execute(query, params)
        results = cursor.fetchall()

        # Convert results to a list of dictionaries
        data = [dict(zip([col[0] for col in cursor.description], row)) for row in results]
        return jsonify({"TopSkills": data}), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching top skills: {e}")
        return jsonify({"error": str(e)}), 500

@analyst.route('/application_success_rate/<industry>', methods=['GET'])
def get_application_success_rate(industry):
    try:
        cursor = db.get_db().cursor()

        # Query to calculate the application success rate
        query = """
            SELECT
                COUNT(CASE WHEN a.Status = 'Accepted' THEN 1 END) AS AcceptedApplications,
                COUNT(a.ApplicantID) AS TotalApplications
            FROM Applicant a
            JOIN JobListing j ON a.JobID = j.JobID
            JOIN Industry i ON j.IndustryID = i.IndustryID
        """
        params = []

        if industry != "All Industries":
            query += " WHERE i.IndustryName = %s"
            params.append(industry)

        cursor.execute(query, params)
        result = cursor.fetchone()

        accepted, total = result
        success_rate = (accepted / total) * 100 if total > 0 else 0

        return jsonify({"ApplicationSuccessRate": success_rate}), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching application success rate: {e}")
        return jsonify({"error": str(e)}), 500
