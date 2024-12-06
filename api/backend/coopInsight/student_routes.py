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
student = Blueprint('student', __name__)

# Route 1: GET all students
@student.route('/students', methods=['GET'])
def get_students():

    cursor = db.get_db().cursor()
    cursor.execute('''
                    SELECT * FROM students
                    ''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Route 2: GET a single student by ID, including their applications
@student.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
                        SELECT * FROM students WHERE id = {student_id}
                        ''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Route 3: POST a new student
@student.route('/students', methods=['POST'])
def add_student():
    cursor = db.get_db().cursor()
    cursor.execute('''
                        INSERT INTO students (name, age, major, gpa)
                        VALUES ('{data["name"]}', {data["age"]}, '{data["major"]}', {data["gpa"]}
                        ''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Route 4: PUT to update a student's GPA
@student.route('/students/<int:student_id>', methods=['PUT'])
def update_student_gpa(student_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
                        UPDATE students SET gpa = {data['gpa']} WHERE id = {student_id}
                        ''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Route 5: DELETE a student's rating on a company
@student.route('/students/<int:student_id>/ratings/<int:company_id>', methods=['DELETE'])
def delete_student_rating(student_id, company_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
                        DELETE FROM applications WHERE student_id = {student_id} AND company_id = {company_id} AND rating IS NOT NULL
                        ''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Route 6: GET students with a GPA above a certain value
@student.route('/students/gpa/<float:min_gpa>', methods=['GET'])
def get_students_by_gpa(min_gpa):
    cursor = db.get_db().cursor()
    cursor.execute('''
                        SELECT * FROM students WHERE gpa > {min_gpa}
                        ''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Route 7: GET students with a certain number of applications
@student.route('/students/applications/<int:num_apps>', methods=['GET'])
def get_students_by_applications(num_apps):
    cursor = db.get_db().cursor()
    cursor.execute('''
                        SELECT s.id, s.name, COUNT(a.id) AS application_count
                        FROM students s
                        JOIN applications a ON s.id = a.student_id
                        GROUP BY s.id, s.name
                        HAVING COUNT(a.id) = {num_apps}
                        ''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Route 8: POST to enroll a student in a company application
@student.route('/students/<int:student_id>/applications', methods=['POST'])
def add_application(student_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
                        INSERT INTO applications (student_id, company_id, status, rating)
                        VALUES ({student_id}, {data["company_id"]}, '{data["status"]}', {data.get("rating", "NULL")}
                        ''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Route 9: PATCH to update a student’s major
@student.route('/students/<int:student_id>/major', methods=['PATCH'])
def update_student_major(student_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
                        UPDATE students SET major = '{data['major']}' WHERE id = {student_id}
                        ''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Route 10: GET companies where students have submitted applications, grouped by company name
@student.route('/students/applications/companies', methods=['GET'])
def get_application_companies():
    cursor = db.get_db().cursor()
    cursor.execute('''
                        SELECT c.name, COUNT(a.id) AS application_count
                        FROM companies c
                        JOIN applications a ON c.id = a.company_id
                        GROUP BY c.name
                        ''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Route 11: DELETE all applications for a specific student
@student.route('/students/<int:student_id>/applications', methods=['DELETE'])
def delete_all_applications(student_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
                        DELETE FROM applications WHERE student_id = {student_id}
                        ''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response
