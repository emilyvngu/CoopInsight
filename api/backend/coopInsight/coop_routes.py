########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
import sys
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


def debug(s):
    print('PPP', s, file=sys.stderr)

@coop.route('/updateUser', methods=['PUT'])
def update_user():

    user = request.form

    debug(user)

    id = user['UserID']
    first = user['FirstName']
    last = user['LastName']
    email = user['Email'] 
    password = user['Password']
    phone = user['PhoneNumber']

    cursor = db.get_db().cursor()

    query = f'''
                   INSERT
                   INTO User (UserID, FirstName, LastName, Email, Password, PhoneNumber, AccessLevel)
                   VALUES ('{id}', '{first}', '{last}', '{email}', '{password}', '{phone}', 'User');
                   '''
    
    debug(query)

    cursor.execute(query) 
    
    db.get_db().commit()

    response = make_response('Successfully Added User')
    response.status_code = 200
    return response

@coop.route('/lastUserID', methods=['GET'])
def get_last_user_id():
    cursor = db.get_db().cursor()
    cursor.execute('''
                   SELECT UserID
                   FROM User
                   ORDER BY UserID DESC
                   LIMIT 1
                   ''')
    
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200

    return the_response


@coop.route('/jobListings', methods=['GET'])
def get_job_listings():
    cursor = db.get_db().cursor()
    cursor.execute('''
                   SELECT JobID, Name, Major, MinGPA 
                   FROM JobListing
                   ORDER BY JobID
                   ''')
    
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200

    return the_response


@coop.route('/jobListingDetails')
def get_specific_listing():
    
    user = request.form

    id = user['JobID']

    cursor = db.get_db().cursor()

    query = f'''
            SELECT * 
            FROM JobListing
            WHERE JobID = '{id}'
            '''
    
    debug(query)
    
    cursor.execute(query)

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200

    return the_response

@coop.route('/getIndustry', methods= ['GET'])
def get_industry_id():

    user = request.form

    id = user['IndustryID']

    cursor = db.get_db().cursor()

    query = f'''
            SELECT IndustryName
            FROM Industry
            WHERE IndustryID = '{id}'
            '''
    
    cursor.execute(query)

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200

    return the_response

@coop.route('/getCompany', methods= ['GET'])
def get_company_id():

    user = request.form

    id = user['CompanyID']

    cursor = db.get_db().cursor()

    query = f'''
            SELECT CompanyName
            FROM Company
            WHERE CompanyID = '{id}'
            '''
    
    cursor.execute(query)

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200

    return the_response

@coop.route('/getSkill', methods= ['GET'])
def get_skill_id():

    user = request.form

    id = user['SkillID']

    cursor = db.get_db().cursor()

    query = f'''
            SELECT SkillName
            FROM Skill
            WHERE SkillID = '{id}'
            '''
    
    cursor.execute(query)

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200

    return the_response