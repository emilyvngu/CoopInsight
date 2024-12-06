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
