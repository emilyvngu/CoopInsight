########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
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


@coop.route('/jobListingDetails', methods=['GET'])
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

@coop.route('/applyToJob', methods=['PUT'])
def apply_to_job():
    user = request.form

    jobID = user['JobID']

    studentID = user['StudentID']

    cursor = db.get_db().cursor()
    logger.info(f'Applying to job {jobID} as student {studentID}')

    query = f'''
            INSERT INTO
            Applicant (StudentID, JobID)
            VALUES ('{studentID}', '{jobID}')
            '''
    
    cursor.execute(query)

    db.get_db().commit()

    response = make_response('Successfully Applied!')
    response.status_code = 200

    return response


@coop.route('/lastStudentID', methods=['GET'])
def get_last_student_id():
    cursor = db.get_db().cursor()
    cursor.execute('''
                   SELECT StudentID
                   FROM Student
                   ORDER BY StudentID DESC
                   LIMIT 1
                   ''')
    
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200

    return the_response

@coop.route('/studentSpecificOffers', methods=['GET'])
def get_student_specific_offers():
    user = request.form

    applicantID = user['StudentID']

    cursor = db.get_db().cursor()

    query = f'''
            SELECT Offer.*, Company.CompanyName, JobListing.Name as 'Job Title'
            FROM Offer
            INNER JOIN JobListing ON Offer.JobID = JobListing.JobID
            INNER JOIN Company ON JobListing.CompanyID = Company.CompanyID
            WHERE ApplicantID = '{applicantID}'
            '''
    
    debug(query)
    
    cursor.execute(query)

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200

    return the_response

@coop.route('/withdrawOfferFromStudent', methods=['DELETE'])
def withdraw_offer_from_student():
    user = request.form

    offerID = user['OfferID']

    query = f'''
            DELETE FROM Offer
            WHERE OfferID = '{offerID}'
            '''

    cursor = db.get_db().cursor()

    cursor.execute(query)

    db.get_db().commit()

    theResponse = make_response('Withdrawn!')
    theResponse.status_code = 200

    return theResponse

@coop.route('/getCompanyOffers', methods=['GET'])
def get_company_offers():
    data = request.form

    CompanyID = data['CompanyID']

    cursor = db.get_db().cursor()

    query = f'''
            SELECT Offer.*, User.UserID, User.FirstName, User.LastName, JobListing.Name as JobListing, JobListing.JobID
            FROM Offer
            NATURAL JOIN JobListing
            INNER JOIN Student ON Offer.ApplicantID = Student.StudentID
            INNER JOIN User ON Student.UserID = User.UserID
            WHERE CompanyID = '{CompanyID}'
            ORDER BY OfferDate DESC
            '''

    cursor.execute(query)

    theData = cursor.fetchall()

    theResponse = make_response(jsonify(theData))
    theResponse.status_code = 200

    return theResponse

@coop.route('/acceptOffer', methods=['PUT'])
def accept_offer():
    user = request.form

    offerID = user['OfferID']

    query = f'''
            UPDATE Offer
            SET Status = 'Accepted'
            WHERE OfferID = '{offerID}'
            '''
    
    cursor = db.get_db().cursor()

    cursor.execute(query)

    db.get_db().commit()

    theResponse = make_response('Accepted!')
    theResponse.status_code = 200

    return theResponse

@coop.route('/rejectOffer', methods=['PUT'])
def reject_offer():
    user = request.form

    offerID = user['OfferID']

    query = f'''
            UPDATE Offer
            SET Status = 'Rejected'
            WHERE OfferID = '{offerID}'
            '''
    
    cursor = db.get_db().cursor()

    cursor.execute(query)

    db.get_db().commit()

    theResponse = make_response('Rejected!')
    theResponse.status_code = 200

    return theResponse

@coop.route('/resetOffer', methods=['PUT'])
def reset_offer():
    user = request.form

    offerID = user['OfferID']

    query = f'''
            UPDATE Offer
            SET Status = 'Pending'
            WHERE OfferID = '{offerID}'
            '''
    
    cursor = db.get_db().cursor()

    cursor.execute(query)

    db.get_db().commit()

    theResponse = make_response('Reset!')
    theResponse.status_code = 200

    return theResponse

@coop.route('/getEmployeeCompany', methods=['GET'])
def get_employee_company():
    user = request.form

    employeeID = user['EmployeeID']

    query = f'''
            SELECT Employee.CompanyID, CompanyName
            FROM Employee
            INNER JOIN Company ON Employee.CompanyID = Company.CompanyID
            WHERE EmployeeID = '{employeeID}'
            '''
    
    cursor = db.get_db().cursor()

    cursor.execute(query)

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200

    return the_response

@coop.route('/getCompanyJobListings', methods=['GET'])
def get_company_jobs():
    user = request.form

    companyID = user['CompanyID']


    query = f'''
            SELECT *
            FROM JobListing
            WHERE CompanyID = '{companyID}'
            '''
    
    cursor = db.get_db().cursor()

    cursor.execute(query)

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200

    return the_response

@coop.route('/getCompanyJobApplicants', methods= ['GET'])
def get_company_job_applicants():
    user = request.form

    jobID = user['JobID']

    query = f'''
            SELECT Applicant.ApplicantID, Applicant.JobID, Applicant.Status, Student.*, User.FirstName, User.LastName
            FROM Applicant
            NATURAL JOIN Student
            NATURAL JOIN User
            WHERE JobID = '{jobID}'
            '''
    
    cursor = db.get_db().cursor()

    cursor.execute(query)

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200

    return the_response

@coop.route('/getApplicantProfile', methods= ['GET'])
def get_applicant_profile():
    user = request.form

    studentID = user['StudentID']

    query = f'''
            SELECT *
            FROM Student
            WHERE StudentID = '{studentID}'
            '''
    
    cursor = db.get_db().cursor()

    cursor.execute(query)

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200

    return the_response

@coop.route('/getStudentUserDetails', methods= ['GET'])
def get_student_user_details():
    user = request.form

    userID = user['UserID']

    query = f'''
            SELECT *
            FROM User
            WHERE UserID = '{userID}'
            '''
    
    debug(query)

    cursor = db.get_db().cursor()

    cursor.execute(query)

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200

    return the_response

@coop.route('/makeOffer', methods=['PUT'])
def make_an_offer():
    user = request.form

    jobID = user['JobID']
    appID = user['ApplicantID']

    wage = user['Wage']
    start = user['StartDate']
    end = user['EndDate']


    cursor = db.get_db().cursor()

    query = f'''
            INSERT INTO
            Offer (ApplicantID, JobID, Wage, StartDate, EndDate)
            VALUES ('{appID}', '{jobID}', '{wage}', '{start}', '{end}')
            '''
    
    cursor.execute(query)

    db.get_db().commit()

    response = make_response('Successfully Applied!')
    response.status_code = 200

    return response

@coop.route('/updateApplicant', methods=['PUT'])
def update_applicant():

    user = request.form

    appID = user['ApplicantID']

    query = f'''
            UPDATE Applicant
            SET Status = 'Offered'
            WHERE ApplicantID = '{appID}'
            '''
    
    cursor = db.get_db().cursor()

    cursor.execute(query)

    db.get_db().commit()

    theResponse = make_response('Accepted!')
    theResponse.status_code = 200

    return theResponse

@coop.route('/getMajors', methods=['GET'])
def get_majors():

    cursor = db.get_db().cursor()

    query = f'''
            SELECT Major
            FROM StudentMajor;
            '''

    cursor.execute(query)

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200

    return the_response

@coop.route('/postJobOffer', methods=['PUT'])
def post_job_offer():
    user = request.form

    name = user['Position']
    companyID = user['CompanyID']
    major = user['Major']
    minGPA = user['MinGPA']
    industryID = user['IndustryID']
    description = user['JobDescription']
    skill = user['SkillID']

    query = f'''
            INSERT INTO
            JobListing (Name, CompanyID, Major, MinGPA, IndustryID, JobDescription, SkillID)
            VALUES ('{name}', '{companyID}', '{major}', '{minGPA}', '{industryID}', '{description}', '{skill}')
    '''

    cursor = db.get_db().cursor()

    cursor.execute(query)

    db.get_db().commit()

    theResponse = make_response('Posted!')
    theResponse.status_code = 200

    return theResponse


@coop.route('/hireStudent', methods=['POST'])
def hire_student():
    data = request.form

    offer_id = data['OfferID']
    applicant_id = data['ApplicantID']


    query = f'''
            UPDATE Applicant
            SET Status = 'Hired'
            WHERE ApplicantID = '{applicant_id}'
            '''

    cursor = db.get_db().cursor()

    cursor.execute(query)

    query = f'''
            DELETE FROM Offer
            WHERE OfferID = '{offer_id}'
            '''

    cursor.execute(query)

    query = f'''
        INSERT INTO Employee (UserID, CompanyID, JobID)
        VALUES ('{data['HireID']}', '{data['CompanyID']}', '{data['JobID']}')
        '''

    cursor.execute(query)

    db.get_db().commit()

    theResponse = make_response('Hired!')
    theResponse.status_code = 200

    return theResponse


@coop.route('/getEmployeeInfo', methods=['GET'])
def get_employee_info():
    data = request.form

    user_id = data['UserID']

    query = f'''
            SELECT EmployeeID, Company.CompanyID, JobID, CompanyName
            FROM Employee
            INNER JOIN Company ON Employee.CompanyID = Company.CompanyID
            WHERE UserID = '{user_id}'
            '''

    cursor = db.get_db().cursor()

    cursor.execute(query)

    theData = cursor.fetchall()

    if len(theData) == 0:
        resp = make_response('No Employee Found')
        resp.status_code = 404
        return resp

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200

    return the_response


@coop.route('/resign', methods=['DELETE'])
def resign():
    data = request.form

    employee_id = data['EmployeeID']

    query = f'''
            DELETE FROM Employee
            WHERE EmployeeID = '{employee_id}'
            '''

    cursor = db.get_db().cursor()

    cursor.execute(query)

    db.get_db().commit()

    theResponse = make_response('Resigned!')
    theResponse.status_code = 200

    return theResponse


@coop.route('/getEmployees', methods=['GET'])
def get_employees():
    data = request.form

    companyID = data['CompanyID']

    query = f'''
            SELECT Employee.EmployeeID, User.FirstName, User.LastName, JobListing.Name as JobListing
            FROM Employee
            INNER JOIN User ON Employee.UserID = User.UserID
            INNER JOIN JobListing ON Employee.JobID = JobListing.JobID
            WHERE Employee.CompanyID = '{companyID}'
            '''

    cursor = db.get_db().cursor()

    cursor.execute(query)

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200

    return the_response


@coop.route('/terminateEmployee', methods=['DELETE'])
def terminate_employee():
    data = request.form

    employeeID = data['EmployeeID']

    query = f'''
            DELETE FROM Employee
            WHERE EmployeeID = '{employeeID}'
            '''

    cursor = db.get_db().cursor()

    cursor.execute(query)

    db.get_db().commit()

    theResponse = make_response('Terminated!')
    theResponse.status_code = 200

    return theResponse


#     CREATE TABLE IF NOT EXISTS JobListing
# (
#     JobID          INT PRIMARY KEY AUTO_INCREMENT,
#     Name           VARCHAR(50)  NOT NULL,
#     CompanyID      INT          NOT NULL REFERENCES Company (CompanyID) ON UPDATE CASCADE ON DELETE CASCADE,
#     Major          VARCHAR(50)  NOT NULL REFERENCES StudentMajor (Major) ON UPDATE CASCADE ON DELETE CASCADE,
#     MinGPA         FLOAT(4)     NOT NULL,
#     IndustryID     INT          NOT NULL REFERENCES Industry (IndustryID) ON UPDATE CASCADE ON DELETE RESTRICT,
#     Posted         DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     JobDescription VARCHAR(500) NOT NULL,
#     SkillID        INT          NOT NULL REFERENCES Skill (SkillID) ON UPDATE CASCADE ON DELETE RESTRICT
# );