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

"""
(
    RatingID                    INT PRIMARY KEY AUTO_INCREMENT,
    OverallRating               INT          NOT NULL,
    Review                      VARCHAR(500) NOT NULL,
    WorkCultureRating           INT          NOT NULL,
    CompensationRating          INT          NOT NULL,
    WorkLifeBalanceRating       INT          NOT NULL,
    LearningOpportunitiesRating INT          NOT NULL,
    JobID                       INT REFERENCES JobListing (JobID) ON UPDATE CASCADE ON DELETE CASCADE,
    CompanyID                   INT REFERENCES Company (CompanyID) ON UPDATE CASCADE ON DELETE CASCADE,
    UserID                      INT          NOT NULL REFERENCES User (UserID) ON UPDATE CASCADE ON DELETE CASCADE
);"""


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


"""
CREATE TABLE IF NOT EXISTS Company
(
    CompanyID          INT PRIMARY KEY AUTO_INCREMENT,
    CompanyName        VARCHAR(50)  NOT NULL,
    IndustryID         INT          NOT NULL REFERENCES Industry (IndustryID) ON UPDATE CASCADE ON DELETE RESTRICT,
    CompanyDescription VARCHAR(500) NOT NULL,
    AdminID            INT          NOT NULL REFERENCES `User` (UserID) ON UPDATE CASCADE ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS JobListing
(
    JobID          INT PRIMARY KEY AUTO_INCREMENT,
    Name           VARCHAR(50)  NOT NULL,
    CompanyID      INT          NOT NULL REFERENCES Company (CompanyID) ON UPDATE CASCADE ON DELETE CASCADE,
    Major          VARCHAR(50)  NOT NULL REFERENCES StudentMajor (Major) ON UPDATE CASCADE ON DELETE CASCADE,
    MinGPA         FLOAT(4)     NOT NULL,
    IndustryID     INT          NOT NULL REFERENCES Industry (IndustryID) ON UPDATE CASCADE ON DELETE RESTRICT,
    Posted         DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    JobDescription VARCHAR(500) NOT NULL,
    SkillID        INT          NOT NULL REFERENCES Skill (SkillID) ON UPDATE CASCADE ON DELETE RESTRICT
"""