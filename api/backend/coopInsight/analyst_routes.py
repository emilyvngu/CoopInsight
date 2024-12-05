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
analyst = Blueprint('coop', __name__)


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
