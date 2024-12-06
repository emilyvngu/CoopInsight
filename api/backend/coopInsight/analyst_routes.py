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

        the_response = make_response(jsonify(theData))
        the_response.status_code = 200
        return response

    except Exception as e:
        print(f"Error fetching industries in jobs: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@analyst.route('/available_positions', methods=['GET'])
def get_available_positions():
    time_period = request.args.get('time_period')
    industry = request.args.get('industry')

    query = """
        SELECT COUNT(*) AS TotalPositions
        FROM JobListing j
        WHERE j.Posted >= NOW() - INTERVAL %s
    """
    params = ["12 MONTH"] if time_period == "Last 12 Months" else ["6 MONTH"]
    if industry != "All Industries":
        query += " AND j.IndustryID = (SELECT IndustryID FROM Industry WHERE IndustryName = %s)"
        params.append(industry)

    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()
    return jsonify({"data": {"total_positions": result[0]}})

@analyst.route('/top_skills', methods=['GET'])
def get_top_skills():
    time_period = request.args.get('time_period')
    industry = request.args.get('industry')

    query = """
        SELECT s.SkillName, COUNT(js.SkillID) AS Count
        FROM JobSkill js
        JOIN Skill s ON js.SkillID = s.SkillID
        JOIN JobListing j ON js.JobID = j.JobID
        WHERE j.Posted >= NOW() - INTERVAL %s
    """
    params = ["12 MONTH"] if time_period == "Last 12 Months" else ["6 MONTH"]
    if industry != "All Industries":
        query += " AND j.IndustryID = (SELECT IndustryID FROM Industry WHERE IndustryName = %s)"
        params.append(industry)

    query += " GROUP BY s.SkillName ORDER BY Count DESC LIMIT 10"
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    return jsonify({"data": [dict(zip([col[0] for col in cursor.description], row)) for row in results]})

@analyst.route('/application_success_rate', methods=['GET'])
def get_application_success_rate():
    time_period = request.args.get('time_period')
    industry = request.args.get('industry')

    query = """
        SELECT 
            SUM(CASE WHEN a.Status = 'Accepted' THEN 1 ELSE 0 END) AS Success,
            SUM(CASE WHEN a.Status != 'Accepted' THEN 1 ELSE 0 END) AS Failure
        FROM Applicant a
        JOIN JobListing j ON a.JobID = j.JobID
        WHERE j.Posted >= NOW() - INTERVAL %s
    """
    params = ["12 MONTH"] if time_period == "Last 12 Months" else ["6 MONTH"]
    if industry != "All Industries":
        query += " AND j.IndustryID = (SELECT IndustryID FROM Industry WHERE IndustryName = %s)"
        params.append(industry)

    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()
    return jsonify({"data": {"success": result[0], "failure": result[1]}})

