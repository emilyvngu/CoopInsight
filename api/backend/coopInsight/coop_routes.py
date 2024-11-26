########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
coop = Blueprint('coop', __name__)


#------------------------------------------------------------
# Get all customers from the system
@coop.route('/user', methods=['GET'])
def get_users():

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT UserID, FirstName, LastName,
                    Email, Password, PhoneNumber, AccessLevel FROM User
                    ORDER BY UserID
                   ''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@coop.route('/skill', methods=['GET'])
def get_skills():

    cursor = db.get_db().cursor()
    cursor.execute('''
                   SELECT SkillID, SkillName
                   FROM Skill
                   ORDER BY SkillID
                   ''')
    
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200

    return the_response

@coop.route('/industry', methods=['GET'])
def get_industries():

    cursor = db.get_db().cursor()
    cursor.execute('''
                   SELECT IndustryID, IndustryName
                   FROM Industry
                   ORDER BY IndustryID
                   ''')
    
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200

    return the_response