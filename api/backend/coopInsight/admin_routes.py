########################################################
# Admin blueprint of endpoints
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

#------------------------------------------------------------
# Create a new Blueprint object
admin = Blueprint('admin', __name__)


#------------------------------------------------------------
@admin.route('/error_logs', methods=['GET'])
def get_error_logs():
    """
    Fetch all error logs from the database.
    """
    try:
        cursor = db.get_db().cursor()
        
        query = """
            SELECT LogID, UserID, ErrorDescription, ErrorDate
            FROM ErrorLog
            ORDER BY ErrorDate DESC
        """
    
        cursor.execute(query)
        theData = cursor.fetchall()

        response = make_response(jsonify(theData))
        response.status_code = 200
        return response

    except Exception as e:
        import traceback
        current_app.logger.error(f"Error fetching error logs: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@admin.route('/flaggedJobs', methods=['GET'])
def get_flagged_jobs():
    cursor = db.get_db().cursor()

    query = """
            SELECT f.FlagID, c.CompanyName, j.Name AS JobName, f.JobID, f.Reason
            FROM FlaggedJob f
            JOIN JobListing j ON f.JobID = j.JobID
            JOIN Company c ON j.CompanyID = c.CompanyID
        """
    
    cursor.execute(query)

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200

    return the_response

@admin.route('/flaggedRatings', methods=['GET'])
def get_flagged_Ratings():
    cursor = db.get_db().cursor()

    query = """
            SELECT f.FlagID, u.FirstName, u.LastName, u.UserID, r.RatingID, r.OverallRating, r.WorkCultureRating,
                r.CompensationRating, r.WorkLifeBalanceRating, r.LearningOpportunitiesRating, r.Review, f.Reason
            FROM FlaggedRating f
            JOIN Rating r on f.RatingID = r.RatingID
            JOIN User u ON r.UserID = u.UserID
        """
    
    cursor.execute(query)

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200

    return the_response

@admin.route('/deleteFlagJob', methods=['DELETE'])
def delete_flag_job():
    data = request.form

    flagID = data['FlagID']

    query = f'''
            DELETE FROM FlaggedJob
            WHERE FlagID = '{flagID}'
            '''
    
    cursor = db.get_db().cursor()

    cursor.execute(query)

    db.get_db().commit()

    theResponse = make_response("Deleted flag!")
    theResponse.status_code = 200

    return theResponse

@admin.route('/deleteFlagRating', methods=['DELETE'])
def delete_flag_rating():
    data = request.form

    flagID = data['FlagID']

    query = f'''
            DELETE FROM FlaggedRating
            WHERE FlagID = '{flagID}'
            '''
    
    cursor = db.get_db().cursor()

    cursor.execute(query)

    db.get_db().commit()

    theResponse = make_response("Deleted flag!")
    theResponse.status_code = 200

    return theResponse


@admin.route('/deleteJob', methods=['DELETE'])
def delete_job():
    data = request.form

    jobID = data['JobID']

    query = f'''
            DELETE FROM JobListing
            WHERE JobID = '{jobID}'
            '''
    
    cursor = db.get_db().cursor()

    cursor.execute(query)

    db.get_db().commit()

    theResponse = make_response("Deleted flag!")
    theResponse.status_code = 200

    return theResponse

@admin.route('/deleteRating', methods=['DELETE'])
def delete_rating():
    data = request.form

    ratingID = data['RatingID']

    query = f'''
            DELETE FROM Rating
            WHERE RatingID = '{ratingID}'
            '''
    
    cursor = db.get_db().cursor()

    cursor.execute(query)

    db.get_db().commit()

    theResponse = make_response("Deleted flag!")
    theResponse.status_code = 200

    return theResponse