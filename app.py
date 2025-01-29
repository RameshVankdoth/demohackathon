#>>>>>>>>>>>>>>>>>>>>>>>>>>============================= System Modules =============================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
import io
import json
import logging
import os
import random
import re
import smtplib
import ssl
import string
import subprocess
import tempfile
import time
import traceback
from datetime import datetime
from html import escape
from html import escape

import pyodbc
import requests
import requests
import schedule
from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient
from dotenv import load_dotenv
from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session, url_for)
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>============= Load environment variables from .env filess============>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
load_dotenv()

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>============================= Configure logging =========================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
logging.basicConfig(
    filename='hackathon.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

log_file_name = "hackathon.log"

#<<<<<<<<<<<<<<<<<<<<<<<============================= Mongodb Configurations =================================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
client = MongoClient(os.environ.get("MONGODB_URI"))

#========================= MongoDB for Problem Statements=======================
db = client[os.environ.get("MONGODB_PROBLEMS_DB")]
collection = db[os.environ.get("MONGODB_PROBLEMS_COLLECTION")]

# =========================MongoDB for Contest Details==========================
db2 = client[os.environ.get("MONGODB_CONTESTS_DB")]
collection2 = db2[os.environ.get("MONGODB_CONTESTS_COLLECTION")]

# ================================Example usage=================================
contests = collection2.find_one({})
psno = contests['psno']


problems = list(collection.find_one({}))

document = collection.find_one({'psno': 11})
test_cases = document.get("test_cases", [])
total_score = 0
document = collection.find_one({'psno': 11})
test_cases = document.get("test_cases", [])
total_score = 0
# <<<<<<<<<<<<<<<<<<<<<<<<<===============================Email configuration===============================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
smtp_port = int(os.environ.get("SMTP_PORT", 587))
smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
email_from = os.environ.get("EMAIL_FROM")
pswd = os.environ.get("EMAIL_PASSWORD")

# <<<<<<<<<<<<<<<<<<<<<<<<<===============================App configuration===============================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
app = Flask(__name__, template_folder="templates")
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx'}
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
#<<<<<<<<<<<<<<<<<<<<<<<============================= Azure Configurations =================================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

AZURE_CONNECTION_STRING = os.environ.get("AZURE_CONNECTION_STRING")
RESUME_CONTAINER_NAME = os.environ.get("RESUME_CONTAINER_NAME")
CODE_CONTAINER_NAME = os.environ.get("CODE_CONTAINER_NAME")
LOG_CONTAINER_NAME = os.environ.get("LOG_CONTAINER_NAME")
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client_resume = blob_service_client.get_container_client(RESUME_CONTAINER_NAME)
container_client_code = blob_service_client.get_container_client(CODE_CONTAINER_NAME)
container_client_logs = blob_service_client.get_container_client(LOG_CONTAINER_NAME)


#====================Functions without any kind of routes enabled===================================
def get_connection():
    logging.info(f'Connecton established with {connection_string}')
    return pyodbc.connect(connection_string)


#============================== OneCompiler API details=============================================
API_URL = "https://onecompiler-apis.p.rapidapi.com/api/v1/run"
HEADERS = {
    "x-rapidapi-key": "45f2a7db9cmsh4284c930ed09c24p1ca7b4jsn10ee469de6e2",
    "x-rapidapi-host": "onecompiler-apis.p.rapidapi.com",
    "Content-Type": "application/json"
}


#====================Functions without any kind of routes enabled===================================
def get_connection():
    logging.info(f'Connecton established with {connection_string}')
    return pyodbc.connect(connection_string)


#============================== OneCompiler API details=============================================
API_URL = "https://onecompiler-apis.p.rapidapi.com/api/v1/run"
HEADERS = {
    "x-rapidapi-key": "45f2a7db9cmsh4284c930ed09c24p1ca7b4jsn10ee469de6e2",
    "x-rapidapi-host": "onecompiler-apis.p.rapidapi.com",
    "Content-Type": "application/json"
}

# ============================SQL Server setup==================================
connection_string = os.environ.get("SQL_CONNECTION_STRING")

#==================================== check file types =============================================
def sanitize_filename(filename):
    return re.sub(r'[^\w\-.]', '', filename).strip()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

#================================== Upload resume in resume blob ===================================
def upload_to_blob(file_stream, filename):
    try:
        logging.info(f"Starting upload for file: {filename}")
        logging.info(f"Starting upload for file: {filename}")
        filename = sanitize_filename(filename)
        logging.debug(f"Sanitized filename: {filename}")
        logging.debug(f"Sanitized filename: {filename}")
        blob_client = blob_service_client.get_blob_client(container=RESUME_CONTAINER_NAME, blob=filename)
        logging.debug("Blob client created")
        logging.debug("Blob client created")
        blob_client.upload_blob(file_stream, blob_type="BlockBlob", overwrite=False)
        logging.info(f"File uploaded successfully: {filename}")
        logging.info(f"File uploaded successfully: {filename}")
        return blob_client.url
    except Exception as e:
        logging.error(f"Error uploading to Azure Blob: {str(e)}", exc_info=True)
        logging.error(f"Error uploading to Azure Blob: {str(e)}", exc_info=True)
        raise


#=============================================Java Headers =============================================================
java_headers = """
import java.util.Scanner;           // For reading input from the console
import java.io.BufferedReader;      // For efficient input reading
import java.io.InputStreamReader;   // For wrapping BufferedReader
import java.io.IOException;         // For handling I/O exceptions
import java.util.StringTokenizer;   // For splitting strings efficiently

import java.util.ArrayList;         // For dynamic arrays
import java.util.LinkedList;        // For linked lists
import java.util.HashSet;           // For sets (no duplicate elements)
import java.util.Set;           // For sets 
import java.util.TreeSet;           // For sorted sets
import java.util.HashMap;           // For hashmaps (key-value pairs)
import java.util.TreeMap;           // For sorted maps
import java.util.PriorityQueue;     // For implementing heaps and priority queues

import java.util.Collections;       // For collection utility methods (sorting, shuffling, etc.)
import java.util.Arrays;            // For array manipulation methods
import java.util.Comparator;        // For custom sorting with comparators
import java.util.stream.Collectors; // For stream operations (filtering, mapping, etc.)
import java.util.stream.Stream;     // For stream operations on collections
import java.util.List;              // For lists (can be ArrayList, LinkedList, etc.)
import java.util.Queue;             // For queue data structures
import java.util.Deque;             // For double-ended queues

// For date and time manipulation
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Solution {
""" 


#=============================================Java Headers =============================================================
java_headers = """
import java.util.Scanner;           // For reading input from the console
import java.io.BufferedReader;      // For efficient input reading
import java.io.InputStreamReader;   // For wrapping BufferedReader
import java.io.IOException;         // For handling I/O exceptions
import java.util.StringTokenizer;   // For splitting strings efficiently

import java.util.ArrayList;         // For dynamic arrays
import java.util.LinkedList;        // For linked lists
import java.util.HashSet;           // For sets (no duplicate elements)
import java.util.Set;           // For sets 
import java.util.TreeSet;           // For sorted sets
import java.util.HashMap;           // For hashmaps (key-value pairs)
import java.util.TreeMap;           // For sorted maps
import java.util.PriorityQueue;     // For implementing heaps and priority queues

import java.util.Collections;       // For collection utility methods (sorting, shuffling, etc.)
import java.util.Arrays;            // For array manipulation methods
import java.util.Comparator;        // For custom sorting with comparators
import java.util.stream.Collectors; // For stream operations (filtering, mapping, etc.)
import java.util.stream.Stream;     // For stream operations on collections
import java.util.List;              // For lists (can be ArrayList, LinkedList, etc.)
import java.util.Queue;             // For queue data structures
import java.util.Deque;             // For double-ended queues

// For date and time manipulation
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Solution {
""" 

#================================== Upload log files in Log blob =======================================
def upload_log_to_blob():
    try:
        unique_filename = generate_unique_filename(log_file_name)
        logging.info(f'Unique file created: {unique_filename}')
        logging.info(f'Unique file created: {unique_filename}')
        unique_filename = sanitize_filename(unique_filename)
        logging.info(f"Starting upload for file: {unique_filename}")
        logging.info(f"Starting upload for file: {unique_filename}")
        blob_client = blob_service_client.get_blob_client(container=LOG_CONTAINER_NAME, blob=unique_filename)
        # Read the log file
        with open(log_file_name, "rb") as data:
            # Upload the log file
            blob_client.upload_blob(data, overwrite=False)
        logging.info(f"Log file uploaded successfully as : {unique_filename}.")
        logging.info(f"Log file uploaded successfully as : {unique_filename}.")

        # Optionally, clear the log file after upload
        with open(log_file_name, 'w'):
            pass
        
    except Exception as e:
        logging.error(f"Error uploading log file: {e}")
        
        
#===================== Generating time name for logs ===========================
def generate_unique_filename(base_name):
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    filename, file_extension = os.path.splitext(base_name)
    return f"{filename}.{current_time}{file_extension}"

    
    
#=============================== Upload code files in Code blob ====================================
def upload_code(file_stream, filename):
    try:
        logging.info(f"Starting upload for file: {filename}")
        logging.info(f"Starting upload for file: {filename}")
        filename = sanitize_filename(filename)
        logging.debug(f"Sanitized filename: {filename}")
        logging.debug(f"Sanitized filename: {filename}")
        blob_client = blob_service_client.get_blob_client(container=CODE_CONTAINER_NAME, blob=filename)
        logging.debug("Blob client created")
        logging.debug("Blob client created")
        blob_client.upload_blob(file_stream, blob_type="BlockBlob", overwrite=False)
        logging.info(f"File uploaded successfully: {filename}")
        logging.info(f"File uploaded successfully: {filename}")
        return blob_client.url
    except Exception as e:
        logging.error(f"Error uploading to Azure Blob: {str(e)}", exc_info=True)
        logging.error(f"Error uploading to Azure Blob: {str(e)}", exc_info=True)
        raise



# ==================================Route for login form============================================

# ==================================Route for login form============================================
@app.route("/login")
def login():
    logging.info("Login page accessed.")
    logging.info("Login page accessed.")
    return render_template("login.html")

#================================= Route for password reset form====================================
#================================= Route for password reset form====================================
@app.route('/resetpass')
def resetpass():
    logging.info("Password reset page accessed.")
    logging.info("Password reset page accessed.")
    return render_template('resetpass.html')


#====================================== login page =================================================
#====================================== login page =================================================
@app.route("/loginpage", methods=["POST", "GET"])
def loginpage():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            logging.info("Login attempt started.")
            logging.info("Login attempt started.")
            conn = get_connection()
            cursor = conn.cursor()

            # Use parameterized query to avoid SQL injection
            cursor.execute("SELECT * FROM Student WHERE EmailId = ?", (email,))
            user = cursor.fetchone()

            if user:
                logging.info(f"User found with email: {email}")
                logging.info(f"User found with email: {email}")
                if check_password_hash(user[5], password):
                    logging.info(f"Password for user {email} is correct.")
                    logging.info(f"Password for user {email} is correct.")

                    # Check if the user has already taken the test
                    cursor.execute("SELECT * FROM Evaluation WHERE StudentID = ?", (user[0],))
                    evals = cursor.fetchall()
                    logging.info(f"User has data as {evals}")
                    logging.info(f"User has data as {evals}")
                    if evals:
                        flash("You have already taken this test.")
                        logging.info(f"User {email} has already taken the test.")
                        logging.info(f"User {email} has already taken the test.")
                        return redirect(url_for("loginpage"))
                    else:
                        # Store user data in session
                        session["user"] = {
                            "user_id": user[0],
                            "fname": user[1],
                            "lname": user[3],
                            "email": user[9],
                            "college": user[14],
                            "mobile": user[10]
                        }

                        logging.info(f"User {email} logged in successfully.")
                        logging.info(f"User {email} logged in successfully.")
                        return redirect(url_for("code"))  # Pass parameters if needed

                else:
                    flash("Invalid email or password. Please try again.")
                    logging.warning(f"Incorrect password entered for user {email}.")
                    logging.warning(f"Incorrect password entered for user {email}.")
                    return redirect(url_for("loginpage"))

            else:
                flash("Invalid email or password. Please try again.")
                logging.warning(f"No user found with email: {email}.")
                logging.warning(f"No user found with email: {email}.")
                return redirect(url_for("loginpage"))

        except Exception as e:
            logging.error(f"An error occurred during login: {str(e)}")
            logging.error(f"An error occurred during login: {str(e)}")
            flash(f"An error occurred: {str(e)}")
            return redirect(url_for("loginpage"))

        finally:
            if 'cursor' in locals():
                cursor.close()
                logging.info("Cursor closed.")
                logging.info("Cursor closed.")
            if 'conn' in locals():
                conn.close()
                logging.info("Connection to SQL server closed.")
                logging.info("Connection to SQL server closed.")

    return render_template("login.html")


#========================================== Function to store the session ==========================
def sessionValidation(session):
    pass


#=========================Route for main landing page no login included=============================
@app.route("/")
@app.route("/home")
def home():
    contests = list(collection2.find({}))
    logging.info(f"Contest found are {contests}")
    return render_template("landingpage.html", contests=contests)


#==================================================== The register page ================================================
#========================================== Function to store the session ==========================
def sessionValidation(session):
    pass


#=========================Route for main landing page no login included=============================
@app.route("/")
@app.route("/home")
def home():
    contests = list(collection2.find({}))
    logging.info(f"Contest found are {contests}")
    return render_template("landingpage.html", contests=contests)


#==================================================== The register page ================================================
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        try:
            logging.info("Registration attempt started.")
            logging.info("Registration attempt started.")
            
            # Extract form data
            fullname = request.form.get("Fullname")
            namelist = list(fullname.split(" "))
            password = request.form.get("Password")
            con_password = request.form.get("Conpass")
            password_hash = generate_password_hash(password)
            fname = namelist[0]
            mname = namelist[1:len(namelist) - 1]
            mname_str = " ".join(mname) if mname else None
            lname = namelist[-1]
            if lname == fname:
                lname = None 
            email = request.form.get("email")
            mobile = request.form.get("mobile")
            gender = request.form.get("gender")
            dob = request.form.get("dob")
            education_level = request.form.get("level")
            college = request.form.get("college")
            marks = request.form.get("marks")
            course = request.form.get("Course")
            specialization = request.form.get("Specialization")
            primary_skill = request.form.get("primarySkill")
            secondary_skill = request.form.get("secondarySkill")
            position_applying = request.form.get("positionApplying")
            alternate_mobile = request.form.get("altphone")
            alternate_email = request.form.get("altemail")
            home_state = int(request.form.get("homeState"))
            home_city = int(request.form.get("homeCity"))
            current_state = int(request.form.get("currState"))
            current_city = int(request.form.get("currCity"))
            preferred_location = request.form.get("prefCity")

            # Get current date and time for DOE
            doe = datetime.now()

            if password != con_password:
                flash("Password does not match.")
                logging.warning("Password confirmation does not match.")
                logging.warning("Password confirmation does not match.")
                return redirect(url_for("register"))

            # Validate if all necessary fields are present
            if not all([fullname, email, mobile, gender, dob, education_level, college, marks, course, specialization, primary_skill, secondary_skill, home_state, home_city, current_state, current_city, preferred_location]):
                flash("Please fill in all required fields.")
                logging.warning("One or more required fields are missing.")
                logging.warning("One or more required fields are missing.")
                return redirect(url_for("register"))

            # Handle file upload
            if 'resume' not in request.files:
                flash('No resume file found.')
                logging.warning("No resume file found in the request.")
                logging.warning("No resume file found in the request.")
                return redirect(url_for('register'))

            file = request.files['resume']
            if file.filename == '':
                flash('No selected file')
                logging.warning("No selected file.")
                logging.warning("No selected file.")
                return redirect(url_for('register'))

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_stream = io.BytesIO(file.read())
                resume_url = upload_to_blob(file_stream, filename)
                logging.info(f"Resume uploaded successfully: {filename}")
                logging.info(f"Resume uploaded successfully: {filename}")
            else:
                flash('Invalid file type')
                logging.warning("Invalid file type for resume.")
                logging.warning("Invalid file type for resume.")
                return redirect(url_for('register'))

            with get_connection() as conn:
                cursor = conn.cursor()

                # Check for existing user
                cursor.execute(
                    "SELECT EmailId, Mobile FROM Student WHERE EmailId = ? OR Mobile = ?",
                    (email, mobile),
                )
                existing_user = cursor.fetchone()
                if existing_user:
                    flash("You are already registered with this email or mobile number.")
                    logging.info(f"Registration attempt with existing email or mobile: {email}, {mobile}")
                    logging.info(f"Registration attempt with existing email or mobile: {email}, {mobile}")
                    return redirect(url_for("register"))

                cursor.execute("SELECT skills FROM def_skills")
                skill_list = cursor.fetchall()
                skills = [skill[0] for skill in skill_list]
                cursor.execute("SELECT CourseID, CourseName FROM Courses")
                courses = cursor.fetchall()
                cursor.execute("SELECT state_id, state_name FROM states")
                states = cursor.fetchall()
                states_list = [{"id": state[0], "name": state[1]} for state in states]
                cursor.execute("SELECT city_id, city_name, state_id FROM cities")
                cities = cursor.fetchall()
                cities_list = [{"id": city[0], "name": city[1], "state_id": city[2]} for city in cities]
                cursor.execute("SELECT LevelID, LevelName FROM EducationLevels")
                levels = cursor.fetchall()
                cursor.execute("SELECT * FROM positions")
                positions_list = cursor.fetchall()
                positions = [{"id": pos[0], "name": pos[1]} for pos in positions_list]
                

                cursor.execute("SELECT skills FROM def_skills")
                skill_list = cursor.fetchall()
                skills = [skill[0] for skill in skill_list]
                cursor.execute("SELECT CourseID, CourseName FROM Courses")
                courses = cursor.fetchall()
                cursor.execute("SELECT state_id, state_name FROM states")
                states = cursor.fetchall()
                states_list = [{"id": state[0], "name": state[1]} for state in states]
                cursor.execute("SELECT city_id, city_name, state_id FROM cities")
                cities = cursor.fetchall()
                cities_list = [{"id": city[0], "name": city[1], "state_id": city[2]} for city in cities]
                cursor.execute("SELECT LevelID, LevelName FROM EducationLevels")
                levels = cursor.fetchall()
                cursor.execute("SELECT * FROM positions")
                positions_list = cursor.fetchall()
                positions = [{"id": pos[0], "name": pos[1]} for pos in positions_list]
                
                # Insert new user
                cursor.execute(
                    "INSERT INTO Student (Fullname, Fname, Mname, Lname, Password, EmailId, Mobile, Gender, DOB, EducationLevel, College, Marks, Course, Specialization, PrimarySkill, SecondarySkill, PositionApplying, AlternateMobile, AlternateEmail, HomeState, HomeCity, CurrentState, CurrentCity, PreferredLocation, DOE, ResumeFilePath) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (fullname, fname, mname_str, lname, password_hash, email, mobile, gender, dob, education_level, college, marks, course, specialization, primary_skill, secondary_skill,
                     position_applying, alternate_mobile, alternate_email, states[home_state-1][1], cities[home_city-1][1], states[current_state-1][1], cities[current_city-1][1], preferred_location, doe, resume_url)
                )
               
                conn.commit()
                logging.info(f"User registered successfully: {email}")
                logging.info(f"User registered successfully: {email}")
                flash("Registration successful")
                return redirect(url_for("loginpage"))

        except Exception as e:
            logging.error(f"An error occurred during registration: {str(e)}")
            logging.error(f"An error occurred during registration: {str(e)}")
            traceback.print_exc()  # Print the full traceback for debugging
            flash(f"An error occurred during registration: {str(e)}")
            return redirect(url_for("register"))

    # Fetch data for the registration form
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT skills FROM def_skills")
            skill_list = cursor.fetchall()
            skills = [skill[0] for skill in skill_list]
            cursor.execute("SELECT CourseID, CourseName FROM Courses")
            courses = cursor.fetchall()
            cursor.execute("SELECT state_id, state_name FROM states")
            states = cursor.fetchall()
            states_list = [{"id": state[0], "name": state[1]} for state in states]
            cursor.execute("SELECT city_id, city_name, state_id FROM cities")
            cities = cursor.fetchall()
            cities_list = [{"id": city[0], "name": city[1], "state_id": city[2]} for city in cities]
            cursor.execute("SELECT LevelID, LevelName FROM EducationLevels")
            levels = cursor.fetchall()
            cursor.execute("SELECT * FROM positions")
            positions_list = cursor.fetchall()
            positions = [{"id": pos[0], "name": pos[1]} for pos in positions_list]
            cursor.execute("SELECT * FROM AvailCities")
            joblocations = cursor.fetchall()
            logging.info("The job locations are:",joblocations)
            logging.info("Form data fetched successfully for registration.")
            cursor.execute("SELECT * FROM AvailCities")
            joblocations = cursor.fetchall()
            logging.info("The job locations are:",joblocations)
            logging.info("Form data fetched successfully for registration.")
    except Exception as e:
        logging.error(f"Database error while fetching form data: {e}")
        logging.error(f"Database error while fetching form data: {e}")
        flash("An error occurred while fetching form data.")
        return render_template("registration.html")

    return render_template("registration.html", skills=skills, courses=courses, levels=levels, cities=cities_list, states=states_list, positions=positions, joblocations=joblocations)
    return render_template("registration.html", skills=skills, courses=courses, levels=levels, cities=cities_list, states=states_list, positions=positions, joblocations=joblocations)


#========================================================= Get the Cities ==============================================
#========================================================= Get the Cities ==============================================
@app.route("/get_cities")
def get_cities():
    state_id = request.args.get("state_id", type=int)
    
    if state_id is None:
        logging.warning("Request received without state_id.")
        logging.warning("Request received without state_id.")
        return jsonify({"cities": []})

    try:
        logging.info(f"Fetching cities for state_id: {state_id}")
        logging.info(f"Fetching cities for state_id: {state_id}")

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT city_id, city_name FROM cities WHERE state_id = ?", (state_id,))
            cities = cursor.fetchall()
            cities_list = [{"id": city[0], "name": city[1]} for city in cities]

            logging.info(f"Cities fetched successfully for state_id: {state_id}")
            logging.info(f"Cities fetched successfully for state_id: {state_id}")

    except Exception as e:
        logging.error(f"Database error while fetching cities for state_id {state_id}: {e}")
        logging.error(f"Database error while fetching cities for state_id {state_id}: {e}")
        return jsonify({"cities": []})

    return jsonify({"cities": cities_list})



# # Logout section to close the user sessions
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))



#=============================== Get the Python function name ========================================
def get_python_function(python_code):
    logging.info("Inside python - name")
    pattern = r'\bdef\s+(\w+)' 
    try:
        match = re.search(pattern, python_code)
        if match:
            function_name = match.group(1)
            logging.info(f"This is the function we got: {function_name}")
            return function_name
        else:
            error_message = "No Python function found."
            logging.error(error_message)
            return error_message
    except Exception as e:
        print("Error is", e)

#=============================== Get the Python function name ========================================
def get_python_function(python_code):
    logging.info("Inside python - name")
    pattern = r'\bdef\s+(\w+)' 
    try:
        match = re.search(pattern, python_code)
        if match:
            function_name = match.group(1)
            logging.info(f"This is the function we got: {function_name}")
            return function_name
        else:
            error_message = "No Python function found."
            logging.error(error_message)
            return error_message
    except Exception as e:
        logging.error(f"An error occurred while getting Python function: {str(e)}", exc_info=True)
        return {"error": f"An unexpected error occurred: {str(e)}"}

#=================== Get the class name from the Java code for compilation ============================
def get_class(java_code):
    logging.info("Inside java - class")
    pattern = r'\bpublic\s+class\s+(\w+)'
    logging.info(f'The code for java is: {java_code}')
    
    try:
        match = re.search(pattern, java_code)
        if match:
            class_name = match.group(1)
            logging.info(f"This is the class we got: {class_name}")
            return class_name
        else:
            error_message = "No Java class found."
            logging.error(error_message)
            return {"error": error_message}
    except Exception as e:
        logging.error(f"An error occurred while getting Java class: {str(e)}", exc_info=True)
        return {"error": f"An unexpected error occurred: {str(e)}"}

#================================= Get class or Function ===========================================

def get_function_or_class(code, language):
    logging.info(f"This is the code inside the get function: {code}")
    logging.info(f'This is the language: {language}')
    try:
        if language=="python":
            logging.info(f"Going for {language} with code: {code}")
            function_name = get_python_function(code)
            if function_name:
                logging.info(f'Got function as {function_name}')
                return ({"function_name":function_name})
            else:
                logging.info(f'No function name found or{code}')
                return ({"error":"Perhaps you forgot to define the function name"})
            
        elif language=="java":
            logging.info(f"This is Java code")
            class_name = get_class(code)
            if class_name:
                logging.info(f'Class is found: {class_name}')
                return ({"class_name":class_name})
            else:
                logging.info("No class found in code")
                return({"error":f"No class defined in this code."})
        else:
            error_message = f"No function or class found for the code"
            logging.info(f"Error occured in line 561: {error_message}")
            return({"error":error_message})
        
    except Exception as e:
        logging.info(f"an exception was cought : {str(e)}")
        return ({"error":f"An error occured as {str(e)}"})





#=================================== Code run with scores ==========================================
def run_code_scores(language, content, file_name):
    payload = {
        "language": language,
        "stdin": "",
        "files": [{"name": file_name, "content": content}]
    }
    logging.info(f"Payload is {payload}")
    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        logging.info(f'Response is {response.json()}')
        stdout = response.json()['stdout']
        if stdout is not None:
            total_score_line = stdout.strip().split('\n')[-1]
            total_score = int(total_score_line)
            logging.info(f'The score is {total_score}')
            logging.info(f'The overall response from the API:{response.json()}')
            return response.json()
        logging.error(f"An error occurred while getting Python function: {str(e)}", exc_info=True)
        return {"error": f"An unexpected error occurred: {str(e)}"}

#=================== Get the class name from the Java code for compilation ============================
def get_class(java_code):
    logging.info("Inside java - class")
    pattern = r'\bpublic\s+class\s+(\w+)'
    logging.info(f'The code for java is: {java_code}')
    
    try:
        match = re.search(pattern, java_code)
        if match:
            class_name = match.group(1)
            logging.info(f"This is the class we got: {class_name}")
            return class_name
        else:
            error_message = "No Java class found."
            logging.error(error_message)
            return {"error": error_message}
    except Exception as e:
        logging.error(f"An error occurred while getting Java class: {str(e)}", exc_info=True)
        return {"error": f"An unexpected error occurred: {str(e)}"}

#================================= Get class or Function ===========================================

def get_function_or_class(code, language):
    logging.info(f"This is the code inside the get function: {code}")
    logging.info(f'This is the language: {language}')
    try:
        if language=="python":
            logging.info(f"Going for {language} with code: {code}")
            function_name = get_python_function(code)
            if function_name:
                logging.info(f'Got function as {function_name}')
                return ({"function_name":function_name})
            else:
                logging.info(f'No function name found or{code}')
                return ({"error":"Perhaps you forgot to define the function name"})
            
        elif language=="java":
            logging.info(f"This is Java code")
            class_name = get_class(code)
            if class_name:
                logging.info(f'Class is found: {class_name}')
                return ({"class_name":class_name})
            else:
                logging.info("No class found in code")
                return({"error":f"No class defined in this code."})
        else:
            error_message = f"No function or class found for the code"
            logging.info(f"Error occured in line 561: {error_message}")
            return({"error":error_message})
        
    except Exception as e:
        logging.info(f"an exception was cought : {str(e)}")
        return ({"error":f"An error occured as {str(e)}"})





#=================================== Code run with scores ==========================================
def run_code_scores(language, content, file_name):
    payload = {
        "language": language,
        "stdin": "",
        "files": [{"name": file_name, "content": content}]
    }
    logging.info(f"Payload is {payload}")
    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        logging.info(f'Response is {response.json()}')
        stdout = response.json()['stdout']
        if stdout is not None:
            total_score_line = stdout.strip().split('\n')[-1]
            total_score = int(total_score_line)
            logging.info(f'The score is {total_score}')
            logging.info(f'The overall response from the API:{response.json()}')
            return response.json()
        else:
            return {'error':'no response recieved from the code'}

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        return {"error": f"HTTP error: {http_err}"}
    except KeyError as key_err:
        logging.error(f"Key error in response: {key_err}")
        return {"error": f"Key error: {key_err}"}
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
        return {"error": f"An unexpected error occurred: {str(e)}"}

#====================================== APIs execution for Code checking ===============================================
def submit_python_code(user_code):
    code = f"""
{user_code}
    """
    function_info = get_function_or_class(code, "python")
    logging.info(f'This is function info {function_info}')
    if "error" in function_info:
        logging.error(function_info["error"])
        return {"error": function_info["error"]}

    function_name = function_info["function_name"]
    content = f"{code}\n\n"
    content += f"test_cases = {test_cases}\n\n"
    content += f"""
# Running test cases
score = 0
for case in test_cases:
    input_value = case['input']
    expected_output = case['output']
    result = {function_name}(input_value)
    if (str(expected_output) == str(result)):
        score += 10
        print("Test Case Passed: Expected Output:", expected_output, "Got:", result, "Score:", score)
    else:
        print("Test Case Passed: Expected Output:", expected_output, "Got:", result, "Score:", 0)
print(score)
"""
    logging.info(f"This is the code:\n{content}")
    return run_code_scores("python", content, f"{function_name}.py")

#===============================================================================

#Send the code for JAVA
def submit_java_code(user_code):
    logging.info(f"Code is in java")
    java_code = f"""
{java_headers}
"""
    class_info = get_function_or_class(java_code, "java")
    logging.info(f'class info : {class_info}')
    if "error" in class_info:
        logging.error(class_info["error"])
        return {"error": class_info["error"]}

    class_name = class_info["class_name"]
    java_code += f"{user_code}\n\n"
    java_code += f"""
public static void main(String[] args) {{
        Object[][] testCases = {{
            {",".join([f"{{{test_case['input']}, {test_case['output']}}}" for test_case in test_cases])}
        }};
        int score = 0;
        for (Object[] testCase : testCases) {{
            int inputValue = (int) testCase[0];
            int expectedOutput = (int) testCase[1];
            int result = {get_class(java_code)}.count(inputValue);
            if(result == expectedOutput){{
                score += 10;
                System.out.println("Test case Passed, Expected Output: " + expectedOutput + ", Got: " + result + "Score:" + score);
            }}else{{
                System.out.println("Test case Failed Expected Output: " + expectedOutput + ", Got: " + result + "Score:" + 0);
            }}            
        }}
        System.out.println(score);
    }}
"""
    java_code += """
}
    """
    logging.info(f'This is the final Code {java_code}')
    return run_code_scores("java", java_code, f"{class_name}.java")

#==================================== Code Running =================================================
def run_code(language, content, file_name):
    payload = {
        "language": language,
        "stdin": "",
        "files": [{"name": file_name, "content": content}]
    }
    logging.info(f"Payload is {payload}")
    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        logging.info(f'Response is {response.json()}')
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        return {"error": f"HTTP error: {http_err}"}
    except KeyError as key_err:
        logging.error(f"Key error in response: {key_err}")
        return {"error": f"Key error: {key_err}"}
            

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        return {"error": f"HTTP error: {http_err}"}
    except KeyError as key_err:
        logging.error(f"Key error in response: {key_err}")
        return {"error": f"Key error: {key_err}"}
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
        return {"error": f"An unexpected error occurred: {str(e)}"}

#====================================== APIs execution for Code checking ===============================================
def submit_python_code(user_code):
    code = f"""
{user_code}
    """
    function_info = get_function_or_class(code, "python")
    logging.info(f'This is function info {function_info}')
    if "error" in function_info:
        logging.error(function_info["error"])
        return {"error": function_info["error"]}

    function_name = function_info["function_name"]
    content = f"{code}\n\n"
    content += f"test_cases = {test_cases}\n\n"
    content += f"""
# Running test cases
score = 0
for case in test_cases:
    input_value = case['input']
    expected_output = case['output']
    result = {function_name}(input_value)
    if (str(expected_output) == str(result)):
        score += 10
        print("Test Case Passed: Expected Output:", expected_output, "Got:", result, "Score:", score)
    else:
        print("Test Case Passed: Expected Output:", expected_output, "Got:", result, "Score:", 0)
print(score)
"""
    logging.info(f"This is the code:\n{content}")
    return run_code_scores("python", content, f"{function_name}.py")

#===============================================================================

#Send the code for JAVA
def submit_java_code(user_code):
    logging.info(f"Code is in java")
    java_code = f"""
{java_headers}
"""
    class_info = get_function_or_class(java_code, "java")
    logging.info(f'class info : {class_info}')
    if "error" in class_info:
        logging.error(class_info["error"])
        return {"error": class_info["error"]}

    class_name = class_info["class_name"]
    java_code += f"{user_code}\n\n"
    java_code += f"""
public static void main(String[] args) {{
        Object[][] testCases = {{
            {",".join([f"{{{test_case['input']}, {test_case['output']}}}" for test_case in test_cases])}
        }};
        int score = 0;
        for (Object[] testCase : testCases) {{
            int inputValue = (int) testCase[0];
            int expectedOutput = (int) testCase[1];
            int result = {get_class(java_code)}.count(inputValue);
            if(result == expectedOutput){{
                score += 10;
                System.out.println("Test case Passed, Expected Output: " + expectedOutput + ", Got: " + result + "Score:" + score);
            }}else{{
                System.out.println("Test case Failed Expected Output: " + expectedOutput + ", Got: " + result + "Score:" + 0);
            }}            
        }}
        System.out.println(score);
    }}
"""
    java_code += """
}
    """
    logging.info(f'This is the final Code {java_code}')
    return run_code_scores("java", java_code, f"{class_name}.java")

#==================================== Code Running =================================================
def run_code(language, content, file_name):
    payload = {
        "language": language,
        "stdin": "",
        "files": [{"name": file_name, "content": content}]
    }
    logging.info(f"Payload is {payload}")
    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        logging.info(f'Response is {response.json()}')
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        return {"error": f"HTTP error: {http_err}"}
    except KeyError as key_err:
        logging.error(f"Key error in response: {key_err}")
        return {"error": f"Key error: {key_err}"}
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
        return {"error": f"An unexpected error occurred: {str(e)}"}
        logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
        return {"error": f"An unexpected error occurred: {str(e)}"}

#====================================== APIs execution for Code Scoring ===============================================
def run_python_code(user_code):
    code = f"""
{user_code}
    """
    function_info = get_function_or_class(code, "python")
    logging.info(f'This is the function info: {function_info} with type {type(function_info)}')

    # Check for errors in function_info
    if 'error' in function_info:
        logging.error(function_info['error'])
        return {"error": function_info['error']}

    function_name = function_info["function_name"]
    content = f"{code}\n\n"
    content += f"test_cases = {test_cases}\n\n"
    content += f"""
# Running test cases
for case in test_cases:
    input_value = case['input']
    expected_output = case['output']
    result = {function_name}(input_value)
    print("Expected Output:", expected_output, "Got:", result)
"""
    logging.info(f'This is the code to be executed:\n{content}')
    return run_code("python", content, f"{function_name}.py")


#===============================================================================

#Send the code for JAVA
def run_java_code(user_code):
    logging.info(f"Code is in java")
    java_code = f"""
{java_headers}
"""
    class_info = get_function_or_class(java_headers, "java")
    logging.info(f'class info : {class_info}')
    if "error" in class_info:
        logging.error(class_info["error"])
        return {"error": class_info["error"]}

    class_name = class_info["class_name"]
    java_code += f"{user_code}\n\n"
    java_code += f"""
public static void main(String[] args) {{
        Object[][] testCases = {{
            {",".join([f"{{{test_case['input']}, {test_case['output']}}}" for test_case in test_cases])}
        }};
        for (Object[] testCase : testCases) {{
            int inputValue = (int) testCase[0];
            int expectedOutput = (int) testCase[1];
            int result = {get_class(java_code)}.count(inputValue);
            System.out.println("Expected Output: " + expectedOutput + ", Got: " + result);
        }}
    }}
"""
    java_code += """
}
    """
    logging.info(f'This is the final Code {java_code}')
    return run_code("java", java_code, f"{class_name}.java")


#========================================= code page ===================================================================

@app.route("/code")
def code():
    if "user" in session:
        try:
            contests = collection2.find_one({})
            psno = contests['psno']
            
            # Fetch the specific problem using psno
            problem = collection.find_one({'psno': psno})
            logging.info(f"The statement is {problem}")
            
            if problem:
                # Fetch and log test cases
                test_cases = problem.get('test_cases', [])
                logging.info(f"The test cases are {test_cases} with type {type(test_cases)}")
                for case in test_cases:
                    print(f"Input: {case['input']}, Output: {case['output']}")
                    
                    logging.info(f'The data type of test case {case["input"]} is {type(case["input"])}')

                    # Convert the input list to a JSON string
                    input_json = json.dumps(case['input'])
                    # Log the data type of the JSON string
                    logging.info(f'The data type of test case input {case["input"]} from json.dumps is {type(input_json)}')

                # Handle HTML content
                problem_statement_html = problem.get('problem_statement', '')
                constraints_html = problem.get('constraints', '')
                explanation_html = problem.get('explanation', '')
                add_info = problem.get('Add_info','')
                
                logging.info(f'The type of problem_statement: {type(problem_statement_html)}')
                logging.info(f'The type of constraints_html: {type(constraints_html)}')
                logging.info(f'The type of explanation_html: {type(explanation_html)}')
                logging.info("Problem exists")
                return render_template(
                    "index.html",
                    user=session["user"],
                    problem=problem,
                    problem_statement=problem_statement_html,
                    constraints=constraints_html,
                    explanation=explanation_html,
                    contests=contests,
                    
                )
            else:
                logging.info("Problem not there")
                flash("Problem not found.")
                return render_template("index.html", user=session["user"], problem=None)
        
        except Exception as e:
            logging.debug(f"An error occurred: {str(e)}")
            flash(f"An error occurred: {str(e)}")
            return render_template("index.html", user=session["user"], problem=None)
    
    else:
        flash("You are not logged in.")
        return redirect(url_for("login"))



#<<<<<<<<<<<<<<<<<<<<<<<<<================================= Code Editor =================================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def store_score(user_id, score, attempt, code):
    try:
        logging.info("Starting the store_score function.")       
        with get_connection() as conn:
            cursor = conn.cursor()           
            if user_id == 'anonymous':
                logging.info("Anonymous user detected; no score stored.")
                return
            user_id = int(user_id) 

            cursor.execute("SELECT StudentID FROM Evaluation")
            existing_ids = [row[0] for row in cursor.fetchall()] 
            if user_id in existing_ids:
                logging.warning(f"User ID {user_id} has already given this test.with attempt {attempt} and code {code}")
                flash("You have already given this test.")
                return
            cursor.execute("INSERT INTO Evaluation (StudentID, Marks, attempt, code) VALUES (?, ?, ?, ?)",
                           (user_id, score, attempt, code))
            conn.commit() 
            logging.info(f"Score of {score} successfully stored for user ID {user_id}.")
    except Exception as e:
        print("Error is", e) 
#====================================== APIs execution for Code Scoring ===============================================
def run_python_code(user_code):
    code = f"""
{user_code}
    """
    function_info = get_function_or_class(code, "python")
    logging.info(f'This is the function info: {function_info} with type {type(function_info)}')

    # Check for errors in function_info
    if 'error' in function_info:
        logging.error(function_info['error'])
        return {"error": function_info['error']}

    function_name = function_info["function_name"]
    content = f"{code}\n\n"
    content += f"test_cases = {test_cases}\n\n"
    content += f"""
# Running test cases
for case in test_cases:
    input_value = case['input']
    expected_output = case['output']
    result = {function_name}(input_value)
    print("Expected Output:", expected_output, "Got:", result)
"""
    logging.info(f'This is the code to be executed:\n{content}')
    return run_code("python", content, f"{function_name}.py")


#===============================================================================

#Send the code for JAVA
def run_java_code(user_code):
    logging.info(f"Code is in java")
    java_code = f"""
{java_headers}
"""
    class_info = get_function_or_class(java_headers, "java")
    logging.info(f'class info : {class_info}')
    if "error" in class_info:
        logging.error(class_info["error"])
        return {"error": class_info["error"]}

    class_name = class_info["class_name"]
    java_code += f"{user_code}\n\n"
    java_code += f"""
public static void main(String[] args) {{
        Object[][] testCases = {{
            {",".join([f"{{{test_case['input']}, {test_case['output']}}}" for test_case in test_cases])}
        }};
        for (Object[] testCase : testCases) {{
            int inputValue = (int) testCase[0];
            int expectedOutput = (int) testCase[1];
            int result = {get_class(java_code)}.count(inputValue);
            System.out.println("Expected Output: " + expectedOutput + ", Got: " + result);
        }}
    }}
"""
    java_code += """
}
    """
    logging.info(f'This is the final Code {java_code}')
    return run_code("java", java_code, f"{class_name}.java")


#========================================= code page ===================================================================

@app.route("/code")
def code():
    if "user" in session:
        try:
            contests = collection2.find_one({})
            psno = contests['psno']
            
            # Fetch the specific problem using psno
            problem = collection.find_one({'psno': psno})
            logging.info(f"The statement is {problem}")
            
            if problem:
                # Fetch and log test cases
                test_cases = problem.get('test_cases', [])
                logging.info(f"The test cases are {test_cases} with type {type(test_cases)}")
                for case in test_cases:
                    print(f"Input: {case['input']}, Output: {case['output']}")
                    
                    logging.info(f'The data type of test case {case["input"]} is {type(case["input"])}')

                    # Convert the input list to a JSON string
                    input_json = json.dumps(case['input'])
                    # Log the data type of the JSON string
                    logging.info(f'The data type of test case input {case["input"]} from json.dumps is {type(input_json)}')

                # Handle HTML content
                problem_statement_html = problem.get('problem_statement', '')
                constraints_html = problem.get('constraints', '')
                explanation_html = problem.get('explanation', '')
                add_info = problem.get('Add_info','')
                
                logging.info(f'The type of problem_statement: {type(problem_statement_html)}')
                logging.info(f'The type of constraints_html: {type(constraints_html)}')
                logging.info(f'The type of explanation_html: {type(explanation_html)}')
                logging.info("Problem exists")
                return render_template(
                    "index.html",
                    user=session["user"],
                    problem=problem,
                    problem_statement=problem_statement_html,
                    constraints=constraints_html,
                    explanation=explanation_html,
                    contests=contests,
                    
                )
            else:
                logging.info("Problem not there")
                flash("Problem not found.")
                return render_template("index.html", user=session["user"], problem=None)
        
        except Exception as e:
            logging.debug(f"An error occurred: {str(e)}")
            flash(f"An error occurred: {str(e)}")
            return render_template("index.html", user=session["user"], problem=None)
    
    else:
        flash("You are not logged in.")
        return redirect(url_for("login"))



#<<<<<<<<<<<<<<<<<<<<<<<<<================================= Code Editor =================================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def store_score(user_id, score, attempt, code):
    try:
        logging.info("Starting the store_score function.")       
        with get_connection() as conn:
            cursor = conn.cursor()           
            if user_id == 'anonymous':
                logging.info("Anonymous user detected; no score stored.")
                return
            user_id = int(user_id) 

            cursor.execute("SELECT StudentID FROM Evaluation")
            existing_ids = [row[0] for row in cursor.fetchall()] 
            if user_id in existing_ids:
                logging.warning(f"User ID {user_id} has already given this test.with attempt {attempt} and code {code}")
                flash("You have already given this test.")
                return
            cursor.execute("INSERT INTO Evaluation (StudentID, Marks, attempt, code) VALUES (?, ?, ?, ?)",
                           (user_id, score, attempt, code))
            conn.commit() 
            logging.info(f"Score of {score} successfully stored for user ID {user_id}.")
    except Exception as e:
        logging.error(f"Database error: {e}", exc_info=True) 

        logging.error(f"Database error: {e}", exc_info=True) 



#============================================= Code with APIs=======================================
@app.route("/execute_code", methods=["POST"])
def execute_code():
    try:
        data = request.json
        code = data.get("code", "")
        language = data.get("language", "")
        user_input = data.get("input", "")
        logging.debug(f'Code to execute: {code}')
        logging.debug(f'User input: {user_input}')
        logging.debug(f'Language: {language}')
        if language == "python":
            result = run_python_code(code)
            if 'error' in result:
                return jsonify({"error": result['error']}), 500
            logging.info('Python result received')

        elif language == "java":
            result = run_java_code(code)
            logging.info('Java result received')
        else:
            return jsonify({"error": f"Unsupported language: {language}"}), 400

        if result.get('status') is not None:
            if result.get('exception') is not None:
                exc_output = result.get('exception')
                return jsonify({"error":exc_output})
            output_lines = result['stdout'].strip().split('\n')
            return jsonify({"output": "\n".join(output_lines)})
    except Exception as e:
        print("Error is", e)
#============================================= Code with APIs=======================================
@app.route("/execute_code", methods=["POST"])
def execute_code():
    try:
        data = request.json
        code = data.get("code", "")
        language = data.get("language", "")
        user_input = data.get("input", "")
        logging.debug(f'Code to execute: {code}')
        logging.debug(f'User input: {user_input}')
        logging.debug(f'Language: {language}')
        if language == "python":
            result = run_python_code(code)
            if 'error' in result:
                return jsonify({"error": result['error']}), 500
            logging.info('Python result received')

        elif language == "java":
            result = run_java_code(code)
            logging.info('Java result received')
        else:
            return jsonify({"error": f"Unsupported language: {language}"}), 400

        if result.get('status') is not None:
            if result.get('exception') is not None:
                exc_output = result.get('exception')
                return jsonify({"error":exc_output})
            output_lines = result['stdout'].strip().split('\n')
            return jsonify({"output": "\n".join(output_lines)})

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({"error": f"Exception: {str(e)}"}), 500




#============================================= Code with APIs=======================================

@app.route("/check_code", methods=["POST"])
def check_code():
    try:
        attempt = 1
        data = request.json
        code = data.get("code", "")
        language = data.get("language", "")
        user_input = data.get("input", "")

        # Retrieve user details from session
        user_id = session.get("user", {}).get("user_id", "anonymous")
        user_fname = session.get("user", {}).get("fname", "anonymous")
        user_lname = session.get("user", {}).get("lname", "anonymous")

        logging.debug(f'Code to execute: {code}')
        logging.debug(f'User input: {user_input}')
        logging.debug(f'Language: {language}')

        # Define the temporary directory
        temp_dir = tempfile.gettempdir()
        logging.debug(f'Temporary directory: {temp_dir}')

        result = {}

        if language == "python":
            # Write code to a temporary Python file
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False, dir=temp_dir) as temp_file:
                temp_file.write(code.encode())
                temp_file.flush()
                temp_file_name = temp_file.name

            logging.debug(f'Temporary file created at: {temp_file_name}')
            result = submit_python_code(code)
            logging.info(f'The result has been received as: {result}')

            if result:
                logging.debug("Inside the result section now sending response to frontend")
                
                if result['stdout'] is not None:
                    output_lines = result['stdout'].strip().split('\n')
                    score = output_lines[-1] if output_lines else "0"
                    # Store score in the database
                    store_score(user_id, score, attempt, temp_file_name)
                    logging.info(f'This is the result line from submit: {output_lines}')
                    logging.info(f'The student got a score of {score}')
                else:
                    return jsonify({"error": "Your code did not generate any output"}), 500

                # Upload to blob
                upload_filename = f"{user_id}_{user_fname}_{user_lname}.py"
                with open(temp_file_name, 'rb') as file_stream:
                    upload_url = upload_code(file_stream, upload_filename)
                    logging.info(f"File uploaded to blob: {upload_url}")

                return jsonify({
                    "output": "\n".join(output_lines),
                    "score": score,
                })

        elif language == "java":
            # Write code to a temporary Java file
            with tempfile.NamedTemporaryFile(suffix=".java", delete=False, dir=temp_dir) as temp_file:
                temp_file.write(code.encode())
                temp_file.flush()
                temp_file_name = temp_file.name

            logging.debug(f'Temporary file created at: {temp_file_name}')
            logging.info("Code is going for Java execution.")
            
            result = submit_java_code(code)
            logging.info(f'The result has been received as: {result}')

            if result:
                logging.debug("Inside the result section now sending response to frontend")
                
                if 'stdout' in result and result['stdout'] is not None:
                    output_lines = result['stdout'].strip().split('\n')
                    score = output_lines[-1] if output_lines else "0"
                    store_score(user_id, score)
                    logging.info(f'This is the result line from submit: {output_lines}')
                    logging.info(f'The student got a score of {score}')
                else:
                    return jsonify({"error": "Your code did not generate any output"}), 500

                # Upload to blob
                upload_filename = f"{user_id}_{user_fname}_{user_lname}.java"
                with open(temp_file_name, 'rb') as file_stream:
                    upload_url = upload_code(file_stream, upload_filename)
                    logging.info(f"File uploaded to blob: {upload_url}")

                # Store score in the database
                

                return jsonify({
                    "output": "\n".join(output_lines),
                    "score": score,
                })

        # Clean up the temporary file
        if 'temp_file_name' in locals():
            os.remove(temp_file_name)

        return jsonify({"error": "No results returned from execution."}), 500

    except KeyError as e:
        logging.error(f"KeyError: {str(e)}")
        return jsonify({"error": f"KeyError: {str(e)}"}), 400
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({"error": f"Exception: {str(e)}"}), 500




#============================================= Code with APIs=======================================

@app.route("/check_code", methods=["POST"])
def check_code():
    try:
        attempt = 1
        data = request.json
        code = data.get("code", "")
        language = data.get("language", "")
        user_input = data.get("input", "")

        # Retrieve user details from session
        user_id = session.get("user", {}).get("user_id", "anonymous")
        user_fname = session.get("user", {}).get("fname", "anonymous")
        user_lname = session.get("user", {}).get("lname", "anonymous")

        logging.debug(f'Code to execute: {code}')
        logging.debug(f'User input: {user_input}')
        logging.debug(f'Language: {language}')

        # Define the temporary directory
        temp_dir = tempfile.gettempdir()
        logging.debug(f'Temporary directory: {temp_dir}')

        result = {}

        if language == "python":
            # Write code to a temporary Python file
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False, dir=temp_dir) as temp_file:
                temp_file.write(code.encode())
                temp_file.flush()
                temp_file_name = temp_file.name

            logging.debug(f'Temporary file created at: {temp_file_name}')
            result = submit_python_code(code)
            logging.info(f'The result has been received as: {result}')

            if result:
                logging.debug("Inside the result section now sending response to frontend")
                
                if result['stdout'] is not None:
                    output_lines = result['stdout'].strip().split('\n')
                    score = output_lines[-1] if output_lines else "0"
                    # Store score in the database
                    store_score(user_id, score, attempt, temp_file_name)
                    logging.info(f'This is the result line from submit: {output_lines}')
                    logging.info(f'The student got a score of {score}')
                else:
                    return jsonify({"error": "Your code did not generate any output"}), 500

                # Upload to blob
                upload_filename = f"{user_id}_{user_fname}_{user_lname}.py"
                with open(temp_file_name, 'rb') as file_stream:
                    upload_url = upload_code(file_stream, upload_filename)
                    logging.info(f"File uploaded to blob: {upload_url}")

                return jsonify({
                    "output": "\n".join(output_lines),
                    "score": score,
                })

        elif language == "java":
            # Write code to a temporary Java file
            with tempfile.NamedTemporaryFile(suffix=".java", delete=False, dir=temp_dir) as temp_file:
                temp_file.write(code.encode())
                temp_file.flush()
                temp_file_name = temp_file.name

            logging.debug(f'Temporary file created at: {temp_file_name}')
            logging.info("Code is going for Java execution.")
            
            result = submit_java_code(code)
            logging.info(f'The result has been received as: {result}')

            if result:
                logging.debug("Inside the result section now sending response to frontend")
                
                if 'stdout' in result and result['stdout'] is not None:
                    output_lines = result['stdout'].strip().split('\n')
                    score = output_lines[-1] if output_lines else "0"
                    store_score(user_id, score)
                    logging.info(f'This is the result line from submit: {output_lines}')
                    logging.info(f'The student got a score of {score}')
                else:
                    return jsonify({"error": "Your code did not generate any output"}), 500

                # Upload to blob
                upload_filename = f"{user_id}_{user_fname}_{user_lname}.java"
                with open(temp_file_name, 'rb') as file_stream:
                    upload_url = upload_code(file_stream, upload_filename)
                    logging.info(f"File uploaded to blob: {upload_url}")

                # Store score in the database
                

                return jsonify({
                    "output": "\n".join(output_lines),
                    "score": score,
                })

        # Clean up the temporary file
        if 'temp_file_name' in locals():
            os.remove(temp_file_name)

        return jsonify({"error": "No results returned from execution."}), 500

    except KeyError as e:
        logging.error(f"KeyError: {str(e)}")
        return jsonify({"error": f"KeyError: {str(e)}"}), 400

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({"error": f"Exception: {str(e)}"}), 500




                   
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({"error": f"Exception: {str(e)}"}), 500




                   
#===================================================Password validation(Vijay gite)=============================================================

#=============================================Generate OTP=============================================
def generate_otp(length=6):
    otp = ''.join(random.choice(string.digits) for _ in range(length))
    logging.info(f'OTP generated: {otp}') 
    logging.info(f'OTP generated: {otp}') 
    return otp
        
#==============================================Sending OTP==============================================
@app.route('/send_otp', methods=['POST'])
def send_otp():
    email_to = request.form['email']
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Student WHERE EmailId = ?", (email_to,))
            user = cursor.fetchone()

            if user:
                otp = generate_otp()
                session['otp'] = otp
                session['user_email'] = email_to
                session['password'] = user[5]
                session['pass1'] = user[6]
                session['pass2'] = user[7]
                session['pass3'] = user[8]

                if all([session.get('pass1'), session.get('pass2'), session.get('pass3')]):
                    logging.warning(f"User with email {email_to} has reached the password reset limit.")
                    logging.warning(f"User with email {email_to} has reached the password reset limit.")
                    flash("You have reached the password reset limit, please contact Artiset.")
                    return redirect(url_for('resetpass'))

                message = f"Subject: Your OTP Code\n\nDear User,\n\nYour OTP code is: {otp}\n\nPlease use this code to complete your verification.\n\nBest regards,\nArtiset Team"

                try:
                    context = ssl.create_default_context()
                    logging.info("Connecting to the SMTP server.")
                    logging.info("Connecting to the SMTP server.")
                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls(context=context)
                        logging.info("Logging in to the SMTP server.")
                        logging.info("Logging in to the SMTP server.")
                        server.login(email_from, pswd)
                        logging.info("Sending email.")
                        logging.info("Sending email.")
                        server.sendmail(email_from, email_to, message)
                    logging.info(f"OTP sent successfully to {email_to}.")
                    logging.info(f"OTP sent successfully to {email_to}.")
                    flash("OTP sent successfully to your email ID.", "success")

                except smtplib.SMTPException as e:
                    logging.error(f"SMTP error occurred: {e}")
                    logging.error(f"SMTP error occurred: {e}")
                    flash("Failed to send OTP. Please check the email address and try again.", "error")
            else:
                logging.warning(f"Email address {email_to} not found.")
                logging.warning(f"Email address {email_to} not found.")
                flash("Email address not found. Please check and try again.", "warning")

    except pyodbc.Error as e:
        logging.error(f"Database error: {e}")
        logging.error(f"Database error: {e}")
        flash("Database error. Please try again later.", "error")

    except Exception as e:
        logging.error(f"General error: {e}")
        logging.error(f"General error: {e}")
        flash("An unexpected error occurred. Please try again later.", "error")

    return redirect(url_for('resetpass'))


#==============================================Verify OTP==============================================

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    user_otp = request.form['otp']
    if 'otp' in session and user_otp == session['otp']:
        logging.info(f"OTP verified successfully for email {session['user_email']}.")
        logging.info(f"OTP verified successfully for email {session['user_email']}.")
        flash("OTP verified successfully.", "success")
        session.pop('otp', None)
        return redirect(url_for('setpass'))
    else:
        logging.warning("Invalid OTP entered.")
        logging.warning("Invalid OTP entered.")
        flash("Invalid OTP. Please try again.", "error")
        return redirect(url_for('resetpass'))


#==========================================Render new pass page=========================================
@app.route('/setpass', methods=['GET'])
def setpass():
    if 'user_email' in session:
        return render_template('setpass.html')
    else:
        logging.warning("Session expired or not found for setpass.")
        logging.warning("Session expired or not found for setpass.")
        flash('Session expired. Please try again.')
        return redirect(url_for('resetpass'))

#============================================Update Password============================================

@app.route('/update_password', methods=['POST'])
def update_password():
    if 'user_email' not in session:
        logging.warning("Session expired during password update.")
        logging.warning("Session expired during password update.")
        flash('Session expired. Please try again.')
        return redirect(url_for('resetpass'))

    email = session['user_email']
    password = session['password']
    pass1 = session['pass1']
    pass2 = session['pass2']
    pass3 = session['pass3']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    if new_password != confirm_password:
        logging.warning("Passwords do not match during password update.")
        logging.warning("Passwords do not match during password update.")
        flash('Passwords do not match.')
        return redirect(url_for('setpass'))

    password_hash = generate_password_hash(new_password)

    if pass1 and pass2 and pass3:
        logging.warning("Password reset limit reached during update.")
        logging.warning("Password reset limit reached during update.")
        flash('You have reached the password reset limit. Please contact Artiset.')
        return redirect(url_for('setpass'))

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Student SET Password = ?, respass3 = respass2, respass2 = respass1, respass1 = ? WHERE EmailId = ?",
                (password_hash, password, email))
            conn.commit()
            logging.info(f"Password updated successfully for email {email}.")
            logging.info(f"Password updated successfully for email {email}.")
            flash('Password updated successfully.')
            session.pop('user_email', None)
            return redirect(url_for('login'))

    except pyodbc.Error as e:
        logging.error(f"Database error occurred during password update: {e}")
        logging.error(f"Database error occurred during password update: {e}")
        flash(f"Database error occurred: {e}")
        return redirect(url_for('setpass'))

    except Exception as e:
        logging.error(f"An error occurred during password update: {e}")
        logging.error(f"An error occurred during password update: {e}")
        flash(f"An error occurred: {e}")
        return redirect(url_for('setpass'))

    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
































# @app.route("/code", methods=["GET"])
# def code():
#     if "user" in session:        
#         try:
#             # Fetch the contest document
#             contests = collection2.find_one({})
#             psno = contests['psno']
            
#             # Fetch the specific problem using psno
#             problem = collection.find({})[psno]  # Modify this query as per your database schema
#             print(problem)

#             if not contests:
#                 flash("Contest not found.")
#                 return redirect(url_for("dashboard"))

#             psno = contests.get('psno')
#             if not psno:
#                 flash("No problem number (psno) found for this contest.")
#                 return redirect(url_for("dashboard"))

#             # Fetch the specific problem using psno
#             problem = collection.find_one({"psno": psno})
#             if not problem:
#                 flash("Problem not found.")
#                 return render_template("index.html", user=session["user"], problem=None)

#             return render_template("index.html", user=session["user"], problem=problem, contests=contests)

#         except Exception as e:
#             flash(f"An error occurred: {str(e)}")
#             return render_template("index.html", user=session["user"], problem=None)

#     else:
#         flash("You are not logged in.")
#         return redirect(url_for("login"))



#================================= Testing the file system =========================================
# @app.route("/test_file_operations")
# def test_file_operations():
#     try:
#         logging.info("Starting file operations.")

#         # Writing to the file
#         with open("testfile.txt", "w") as f:
#             f.write("Test data")
#         logging.info("File 'testfile.txt' written successfully.")

#         # Reading from the file
#         with open("testfile.txt", "r") as f:
#             content = f.read()
#         logging.info("File 'testfile.txt' read successfully.")

#         # Removing the file
#         os.remove("testfile.txt")
#         logging.info("File 'testfile.txt' removed successfully.")

#         return f"File content: {content}"
#     except Exception as e:
#         logging.error(f"Error occurred: {str(e)}")
#         return f"Error: {str(e)}"

# #============================== Testing the subprocess =============================================
# @app.route("/test_subprocess")
# def test_subprocess():
#     try:
#         result = subprocess.run(["echo", "Hello World"], capture_output=True, text=True)
#         return f"stdout: {result.stdout}, stderr: {result.stderr}"
#     except Exception as e:
#         return f"Error: {str(e)}"



# @app.route("/check_code", methods=["POST"])
# def check_code():
#     try:
#         data = request.json
#         code = data["code"]
#         language = data["language"]
#         logging.info(f"Received code for language: {language}")

#         contest = collection2.find_one({})
#         if not contest:
#             logging.error("No contest found in collection2")
#             return jsonify({"error": "No contest found"})

#         psno = contest.get('psno')
#         if psno is None:
#             logging.error("No psno found in contest")
#             return jsonify({"error": "No psno found in contest"})

#         logging.info(f"psno: {psno}")

#         problem = collection.find_one({'psno': psno})
#         if not problem:
#             logging.error(f"No problem found with psno: {psno}")
#             return jsonify({"error": f"No problem found with psno: {psno}"})

#         logging.info(f"Problem statement: {problem.get('problem_statement', 'No problem statement available')}")

#         test_cases = problem.get("test_cases", [])
#         if not test_cases:
#             logging.error(f"No test cases found for problem with psno: {psno}")
#             return jsonify({"error": f"No test cases found for problem with psno: {psno}"})

#         results = []
#         all_passed = True
#         score = 0
    
#         if language == "python":
#             for index, test_case in enumerate(test_cases, start=1):
#                 cus_input = test_case.get("input", "").strip()
#                 logging.info(f"The Custom input fetched is : {cus_input} with data type{type(cus_input)}")
#                 expected_output = test_case.get("output", "").strip()
#                 logging.info(f"The Custom input fetched is : {expected_output} with data type{type(expected_output)}")
#                 logging.info(f'Test Case {index} - Input: {cus_input}, Expected Output: {expected_output}')
#                 result = execute_python(code, cus_input)
#                 actual_output = result["output"]
#                 logging.info(f"the actual output is {actual_output} with data type {type(actual_output)}")
#                 logging.info(f'This is the expected output {expected_output} with data type {type(expected_output)}')
#                 error_message = result.get("error", None)
#                 logging.info(f'This is the error {error_message}')
#                 if error_message:
#                     results.append(f"Test Case {index}: Failed. Error: {0}")
#                 elif str(actual_output) == str(expected_output):
#                     score += 10
#                     results.append(f"Test Case {index}: Passed")
#                 elif actual_output == expected_output:
#                     score += 10
#                     results.append(f"Test Case {index}: Passed")
#                 else:
#                     results.append(f"Test Case {index}: Failed. Got: '{actual_output}', Expected: '{expected_output}'")
#                     all_passed = False

#         elif language == "java":
#             for index, test_case in enumerate(test_cases, start=1):
#                 cus_input = test_case.get("input", "").strip()
#                 expected_output = test_case.get("output", "").strip()
#                 logging.info(f'Test Case {index} - Input: {cus_input}, Expected Output: {expected_output}')
#                 result = execute_java(code, cus_input)
#                 actual_output = result["output"]
#                 logging.info(f"the actual output is {actual_output} with data type {type(actual_output)}")
#                 logging.info(f'This is the expected output {expected_output} with data type {type(expected_output)}')
#                 error_message = result.get("error", None)
#                 error_message = result.get("error", None)
#                 # if error_message:
#                 #     results.append(f"Test Case {index}: Failed. Error: {0}")
#                 #     all_passed = False
#                 if actual_output == expected_output:
#                     score += 10
#                     results.append(f"Test Case {index}: Passed")
#                 elif str(actual_output) == str(expected_output):
#                     score += 10
#                     results.append(f"Test Case {index}: Passed")
#                 else:
#                     results.append(f"Test Case {index}: Failed. Got: '{actual_output}', Expected: '{expected_output}'")
#                     all_passed = False

#         else:
#             return jsonify({"error": f"Unsupported language: {language}"})

#         user_id = session.get('user', {}).get('user_id', 'anonymous')
#         if user_id != 'anonymous':
#             user_id = int(user_id)
        
#         store_score(user_id, score)
#         logging.info(f"Score: {score}, User: {session.get('user', 'anonymous')}")

#         response = {"results": results}
#         if all_passed:
#             session.pop('user', None)
#             response["redirect"] = "/login"
        
#         return jsonify(response)

#     except KeyError as e:
#         logging.error(f"KeyError: {str(e)}")
#         return jsonify({"error": f"KeyError: {str(e)}"})

#     except Exception as e:
#         logging.error(f"Exception: {str(e)}")
#         return jsonify({"error": f"Exception: {str(e)}"})


# #============================================Run code runs here============================================
# @app.route("/execute_code", methods=["POST"])
# def execute_code():
#     try:
        
#         data = request.json
#         code = data.get("code", "")
#         language = data.get("language", "")
#         user_input = data.get("input", "")

#         logging.debug(f'Code to execute: {code}')
#         logging.debug(f'User input: {user_input}')
#         logging.debug(f'Language: {language}')

#         # Define the temporary directory
#         temp_dir = tempfile.gettempdir()
#         logging.debug(f'Temporary directory: {temp_dir}')

#         if language == "python":
#             # Write code to a temporary Python file
#             with tempfile.NamedTemporaryFile(suffix=".py", delete=False, dir=temp_dir) as temp_file:
#                 temp_file.write(code.encode())
#                 temp_file.flush()  # Ensure all data is written to file
#                 temp_file_name = temp_file.name
                
#             logging.debug(f'Temporary file created at: {temp_file_name}')
#             result = subprocess.run(
#                 ["python", temp_file_name],
#                 input=user_input,
#                 capture_output=True,
#                 text=True,
#                 timeout=25
#             )
#             os.remove(temp_file_name)
        
#         elif language == "java":
#             class_name = get_java_class_name(code)  # Implement this function to extract the class name
#             if not class_name:
#                 return jsonify({"error": "Unable to determine the class name from the Java code."})

#             file_name = os.path.join(temp_dir, f"{class_name}.java")
#             with open(file_name, "w") as file:
#                 file.write(code)

#             # Compile the Java code
#             compile_result = subprocess.run(
#                 [javac_path, file_name],
#                 capture_output=True,
#                 text=True
#             )
#             if compile_result.returncode != 0:
#                 os.remove(file_name)  # Cleanup source file on error
#                 return jsonify({"error": compile_result.stderr.strip()})

#             # Run the Java code
#             result = subprocess.run(
#                 [java_path, "-cp", temp_dir, class_name],
#                 input=user_input,
#                 capture_output=True,
#                 text=True,
#                 timeout=10
#             )

#             # Cleanup files
#             os.remove(file_name)
#             os.remove(os.path.join(temp_dir, f"{class_name}.class"))

#             return jsonify({"output": result.stdout.strip(), "error": result.stderr.strip()})
#         else:
#             return jsonify({"error": f"Unsupported language: {language}"})
        
#         # Return the output or error
#         if result.returncode == 0:
#             return jsonify({"output": result.stdout.strip()})
#         else:
#             return jsonify({"error": result.stderr.strip()})
    
#     except KeyError as e:
#         return jsonify({"error": f"KeyError: {str(e)}"})
    
#     except subprocess.CalledProcessError as e:
#         return jsonify({"error": f"CalledProcessError: {str(e)}"})
    
#     except subprocess.TimeoutExpired as e:
#         return jsonify({"error": f"TimeoutExpired: {str(e)}"})
    
#     except Exception as e:
#         return jsonify({"error": f"Exception: {str(e)}"})



# #============================================Submit code runs here============================================
# @app.route("/check_code", methods=["POST"])
# def check_code():
#     try:
#         data = request.json
#         code = data["code"]
#         language = data["language"]
#         logging.info(f"Received code for language: {language}")

#         contest = collection2.find_one({})
#         if not contest:
#             logging.error("No contest found in collection2")
#             return jsonify({"error": "No contest found"})

#         psno = contest.get('psno')
#         if psno is None:
#             logging.error("No psno found in contest")
#             return jsonify({"error": "No psno found in contest"})

#         logging.info(f"psno: {psno}")

#         problem = collection.find_one({'psno': psno})
#         if not problem:
#             logging.error(f"No problem found with psno: {psno}")
#             return jsonify({"error": f"No problem found with psno: {psno}"})

#         logging.info(f"Problem statement: {problem.get('problem_statement', 'No problem statement available')}")

#         test_cases = problem.get("test_cases", [])
#         if not test_cases:
#             logging.error(f"No test cases found for problem with psno: {psno}")
#             return jsonify({"error": f"No test cases found for problem with psno: {psno}"})

#         results = []
#         all_passed = True
#         score = 0
    
#         if language == "python":
#             for index, test_case in enumerate(test_cases, start=1):
#                 cus_input = test_case.get("input", "").strip()
#                 logging.info(f"The Custom input fetched is : {cus_input} with data type{type(cus_input)}")
#                 expected_output = test_case.get("output", "").strip()
#                 logging.info(f"The Custom input fetched is : {expected_output} with data type{type(expected_output)}")
#                 logging.info(f'Test Case {index} - Input: {cus_input}, Expected Output: {expected_output}')
#                 result = execute_python(code, cus_input)
#                 actual_output = result["output"]
#                 logging.info(f"the actual output is {actual_output} with data type {type(actual_output)}")
#                 logging.info(f'This is the expected output {expected_output} with data type {type(expected_output)}')
#                 error_message = result.get("error", None)
#                 logging.info(f'This is the error {error_message}')
#                 if error_message:
#                     results.append(f"Test Case {index}: Failed. Error: {0}")
#                 elif str(actual_output) == str(expected_output):
#                     score += 10
#                     results.append(f"Test Case {index}: Passed")
#                 elif actual_output == expected_output:
#                     score += 10
#                     results.append(f"Test Case {index}: Passed")
#                 else:
#                     results.append(f"Test Case {index}: Failed. Got: '{actual_output}', Expected: '{expected_output}'")
#                     all_passed = False

#         elif language == "java":
#             for index, test_case in enumerate(test_cases, start=1):
#                 cus_input = test_case.get("input", "").strip()
#                 expected_output = test_case.get("output", "").strip()
#                 logging.info(f'Test Case {index} - Input: {cus_input}, Expected Output: {expected_output}')
#                 result = execute_java(code, cus_input)
#                 actual_output = result["output"]
#                 logging.info(f"the actual output is {actual_output} with data type {type(actual_output)}")
#                 logging.info(f'This is the expected output {expected_output} with data type {type(expected_output)}')
#                 error_message = result.get("error", None)
#                 error_message = result.get("error", None)
#                 # if error_message:
#                 #     results.append(f"Test Case {index}: Failed. Error: {0}")
#                 #     all_passed = False
#                 if actual_output == expected_output:
#                     score += 10
#                     results.append(f"Test Case {index}: Passed")
#                 elif str(actual_output) == str(expected_output):
#                     score += 10
#                     results.append(f"Test Case {index}: Passed")
#                 else:
#                     results.append(f"Test Case {index}: Failed. Got: '{actual_output}', Expected: '{expected_output}'")
#                     all_passed = False

#         else:
#             return jsonify({"error": f"Unsupported language: {language}"})

#         user_id = session.get('user', {}).get('user_id', 'anonymous')
#         if user_id != 'anonymous':
#             user_id = int(user_id)
        
#         store_score(user_id, score)
#         logging.info(f"Score: {score}, User: {session.get('user', 'anonymous')}")

#         response = {"results": results}
#         if all_passed:
#             session.pop('user', None)
#             response["redirect"] = "/login"
        
#         return jsonify(response)

#     except KeyError as e:
#         logging.error(f"KeyError: {str(e)}")
#         return jsonify({"error": f"KeyError: {str(e)}"})

#     except Exception as e:
#         logging.error(f"Exception: {str(e)}")
#         return jsonify({"error": f"Exception: {str(e)}"})


# #========================================================= Execute python =========================================================
# def execute_python(code, cus_input):
#     temp_filename = None
#     user_id = session.get('user', {}).get('user_id', 'anonymous')
#     logging.debug(f'Code to execute: {code}')
#     logging.info(f'This is the test case custom :{cus_input}')
#     try:
#         # Create a temporary file for the Python code
#         with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
#             temp_filename = temp_file.name
#             temp_file.write(code.encode('utf-8'))

#         process = subprocess.Popen(
#             ['python', temp_filename],
#             stdin=subprocess.PIPE,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )

#         stdout, stderr = process.communicate(input=cus_input)
#         # return {"output": stdout.strip(), "error": stderr.strip() if stderr else None}
#         return {"output": stdout.strip()}

#     except subprocess.CalledProcessError as e:
#         return {"error": f"CalledProcessError: {str(e)}"}

#     except subprocess.TimeoutExpired as e:
#         return {"error": f"TimeoutExpired: {str(e)}"}

#     except Exception as e:
#         return {"error": f"Exception: {str(e)}"}

#     finally:
#         file_uploaded = False
#         if temp_filename and os.path.exists(temp_filename) and file_uploaded==False:
#             try:
#                 new_filename = f"{user_id}.py" if user_id != 'anonymous' else "anonymous.py"
#                 sanitized_filename = sanitize_filename(new_filename)

#                 os.rename(temp_filename, sanitized_filename)

#                 with open(sanitized_filename, "rb") as file_stream:
#                     file_url = upload_code(file_stream, sanitized_filename)
#                     logging.info(f"File uploaded to: {file_url}")
#                     file_uploaded = True

#             except Exception as e:
#                 logging.error(f"Error during file upload: {str(e)}")

#             finally:
#                 if os.path.exists(sanitized_filename):
#                     os.remove(sanitized_filename)


# #========================================================= Execute Java =========================================================
# def execute_java(code, cus_input):
#     java_filename = None
#     class_filename = None
#     temp_dir = tempfile.gettempdir()
#     logging.debug(f'This is working directory: {temp_dir}')
    
#     try:
#         # Determine the Java class name
#         class_name = get_java_class_name(code)

#         if not class_name:
#             return {"output": "", "error": "Unable to determine the class name from the Java code."}

#         class_filename = os.path.join(temp_dir, f"{class_name}.class")
#         java_filename = os.path.join(temp_dir, f"{class_name}.java")
        
#         logging.info(f'The class file is stored: {class_filename}')
#         logging.info(f'The class file is stored: {java_filename}')
        
#         with open(java_filename, "w") as file:
#             file.write(code)

#         compile_command = ["javac", java_filename]
#         compile_process = subprocess.Popen(
#             compile_command,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )
#         compile_stdout, compile_stderr = compile_process.communicate()

#         if compile_process.returncode != 0:
#             return {"output": "", "error": f"Compilation Error: {compile_stderr.strip()}"}

#         execution_command = ["java", class_name]
#         execution_process = subprocess.Popen(
#             execution_command,
#             stdin=subprocess.PIPE,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )
#         execution_stdout, execution_stderr = execution_process.communicate(input=cus_input)

#         # return {"output": execution_stdout.strip(), "error": execution_stderr.strip() if execution_stderr else None}
#         return {"output": execution_stdout.strip()}

#     except subprocess.CalledProcessError as e:
#         return {"output": "", "error": f"CalledProcessError: {str(e)}"}

#     except subprocess.TimeoutExpired as e:
#         return {"output": "", "error": f"TimeoutExpired: {str(e)}"}

#     except Exception as e:
#         return {"output": "", "error": f"Exception: {str(e)}"}

#     finally:
#         user_id = session.get('user', {}).get('user_id', 'anonymous')
#         if java_filename and os.path.exists(java_filename):
#             try:
#                 new_filename = f"{user_id}.java" if user_id != 'anonymous' else "anonymous.java"
#                 sanitized_filename = sanitize_filename(new_filename)

#                 os.rename(java_filename, sanitized_filename)

#                 with open(sanitized_filename, "rb") as file_stream:
#                     file_url = upload_code(file_stream, sanitized_filename)
#                     logging.info(f"File uploaded to: {file_url}")

#             except Exception as e:
#                 logging.error(f"Error during file upload: {str(e)}")

#             finally:
#                 if os.path.exists(sanitized_filename):
#                     os.remove(sanitized_filename)

#         if class_filename and os.path.exists(class_filename):
#             try:
#                 new_filename = f"{user_id}.class" if user_id != 'anonymous' else "anonymous.class"
#                 sanitized_filename = sanitize_filename(new_filename)

#                 os.rename(class_filename, sanitized_filename)

#                 with open(sanitized_filename, "rb") as file_stream:
#                     file_url = upload_code(file_stream, sanitized_filename)
#                     logging.info(f"File uploaded to: {file_url}")

#             except Exception as e:
#                 logging.error(f"Error during file upload: {str(e)}")

#             finally:
#                 if os.path.exists(sanitized_filename):
#                     os.remove(sanitized_filename)
































# @app.route("/code", methods=["GET"])
# def code():
#     if "user" in session:        
#         try:
#             # Fetch the contest document
#             contests = collection2.find_one({})
#             psno = contests['psno']
            
#             # Fetch the specific problem using psno
#             problem = collection.find({})[psno]  # Modify this query as per your database schema
#             print(problem)

#             if not contests:
#                 flash("Contest not found.")
#                 return redirect(url_for("dashboard"))

#             psno = contests.get('psno')
#             if not psno:
#                 flash("No problem number (psno) found for this contest.")
#                 return redirect(url_for("dashboard"))

#             # Fetch the specific problem using psno
#             problem = collection.find_one({"psno": psno})
#             if not problem:
#                 flash("Problem not found.")
#                 return render_template("index.html", user=session["user"], problem=None)

#             return render_template("index.html", user=session["user"], problem=problem, contests=contests)

#         except Exception as e:
#             flash(f"An error occurred: {str(e)}")
#             return render_template("index.html", user=session["user"], problem=None)

#     else:
#         flash("You are not logged in.")
#         return redirect(url_for("login"))



#================================= Testing the file system =========================================
# @app.route("/test_file_operations")
# def test_file_operations():
#     try:
#         logging.info("Starting file operations.")

#         # Writing to the file
#         with open("testfile.txt", "w") as f:
#             f.write("Test data")
#         logging.info("File 'testfile.txt' written successfully.")

#         # Reading from the file
#         with open("testfile.txt", "r") as f:
#             content = f.read()
#         logging.info("File 'testfile.txt' read successfully.")

#         # Removing the file
#         os.remove("testfile.txt")
#         logging.info("File 'testfile.txt' removed successfully.")

#         return f"File content: {content}"
#     except Exception as e:
#         logging.error(f"Error occurred: {str(e)}")
#         return f"Error: {str(e)}"

# #============================== Testing the subprocess =============================================
# @app.route("/test_subprocess")
# def test_subprocess():
#     try:
#         result = subprocess.run(["echo", "Hello World"], capture_output=True, text=True)
#         return f"stdout: {result.stdout}, stderr: {result.stderr}"
#     except Exception as e:
#         return f"Error: {str(e)}"



# @app.route("/check_code", methods=["POST"])
# def check_code():
#     try:
#         data = request.json
#         code = data["code"]
#         language = data["language"]
#         logging.info(f"Received code for language: {language}")

#         contest = collection2.find_one({})
#         if not contest:
#             logging.error("No contest found in collection2")
#             return jsonify({"error": "No contest found"})

#         psno = contest.get('psno')
#         if psno is None:
#             logging.error("No psno found in contest")
#             return jsonify({"error": "No psno found in contest"})

#         logging.info(f"psno: {psno}")

#         problem = collection.find_one({'psno': psno})
#         if not problem:
#             logging.error(f"No problem found with psno: {psno}")
#             return jsonify({"error": f"No problem found with psno: {psno}"})

#         logging.info(f"Problem statement: {problem.get('problem_statement', 'No problem statement available')}")

#         test_cases = problem.get("test_cases", [])
#         if not test_cases:
#             logging.error(f"No test cases found for problem with psno: {psno}")
#             return jsonify({"error": f"No test cases found for problem with psno: {psno}"})

#         results = []
#         all_passed = True
#         score = 0
    
#         if language == "python":
#             for index, test_case in enumerate(test_cases, start=1):
#                 cus_input = test_case.get("input", "").strip()
#                 logging.info(f"The Custom input fetched is : {cus_input} with data type{type(cus_input)}")
#                 expected_output = test_case.get("output", "").strip()
#                 logging.info(f"The Custom input fetched is : {expected_output} with data type{type(expected_output)}")
#                 logging.info(f'Test Case {index} - Input: {cus_input}, Expected Output: {expected_output}')
#                 result = execute_python(code, cus_input)
#                 actual_output = result["output"]
#                 logging.info(f"the actual output is {actual_output} with data type {type(actual_output)}")
#                 logging.info(f'This is the expected output {expected_output} with data type {type(expected_output)}')
#                 error_message = result.get("error", None)
#                 logging.info(f'This is the error {error_message}')
#                 if error_message:
#                     results.append(f"Test Case {index}: Failed. Error: {0}")
#                 elif str(actual_output) == str(expected_output):
#                     score += 10
#                     results.append(f"Test Case {index}: Passed")
#                 elif actual_output == expected_output:
#                     score += 10
#                     results.append(f"Test Case {index}: Passed")
#                 else:
#                     results.append(f"Test Case {index}: Failed. Got: '{actual_output}', Expected: '{expected_output}'")
#                     all_passed = False

#         elif language == "java":
#             for index, test_case in enumerate(test_cases, start=1):
#                 cus_input = test_case.get("input", "").strip()
#                 expected_output = test_case.get("output", "").strip()
#                 logging.info(f'Test Case {index} - Input: {cus_input}, Expected Output: {expected_output}')
#                 result = execute_java(code, cus_input)
#                 actual_output = result["output"]
#                 logging.info(f"the actual output is {actual_output} with data type {type(actual_output)}")
#                 logging.info(f'This is the expected output {expected_output} with data type {type(expected_output)}')
#                 error_message = result.get("error", None)
#                 error_message = result.get("error", None)
#                 # if error_message:
#                 #     results.append(f"Test Case {index}: Failed. Error: {0}")
#                 #     all_passed = False
#                 if actual_output == expected_output:
#                     score += 10
#                     results.append(f"Test Case {index}: Passed")
#                 elif str(actual_output) == str(expected_output):
#                     score += 10
#                     results.append(f"Test Case {index}: Passed")
#                 else:
#                     results.append(f"Test Case {index}: Failed. Got: '{actual_output}', Expected: '{expected_output}'")
#                     all_passed = False

#         else:
#             return jsonify({"error": f"Unsupported language: {language}"})

#         user_id = session.get('user', {}).get('user_id', 'anonymous')
#         if user_id != 'anonymous':
#             user_id = int(user_id)
        
#         store_score(user_id, score)
#         logging.info(f"Score: {score}, User: {session.get('user', 'anonymous')}")

#         response = {"results": results}
#         if all_passed:
#             session.pop('user', None)
#             response["redirect"] = "/login"
        
#         return jsonify(response)

#     except KeyError as e:
#         logging.error(f"KeyError: {str(e)}")
#         return jsonify({"error": f"KeyError: {str(e)}"})

#     except Exception as e:
#         logging.error(f"Exception: {str(e)}")
#         return jsonify({"error": f"Exception: {str(e)}"})


# #============================================Run code runs here============================================
# @app.route("/execute_code", methods=["POST"])
# def execute_code():
#     try:
        
#         data = request.json
#         code = data.get("code", "")
#         language = data.get("language", "")
#         user_input = data.get("input", "")

#         logging.debug(f'Code to execute: {code}')
#         logging.debug(f'User input: {user_input}')
#         logging.debug(f'Language: {language}')

#         # Define the temporary directory
#         temp_dir = tempfile.gettempdir()
#         logging.debug(f'Temporary directory: {temp_dir}')

#         if language == "python":
#             # Write code to a temporary Python file
#             with tempfile.NamedTemporaryFile(suffix=".py", delete=False, dir=temp_dir) as temp_file:
#                 temp_file.write(code.encode())
#                 temp_file.flush()  # Ensure all data is written to file
#                 temp_file_name = temp_file.name
                
#             logging.debug(f'Temporary file created at: {temp_file_name}')
#             result = subprocess.run(
#                 ["python", temp_file_name],
#                 input=user_input,
#                 capture_output=True,
#                 text=True,
#                 timeout=25
#             )
#             os.remove(temp_file_name)
        
#         elif language == "java":
#             class_name = get_java_class_name(code)  # Implement this function to extract the class name
#             if not class_name:
#                 return jsonify({"error": "Unable to determine the class name from the Java code."})

#             file_name = os.path.join(temp_dir, f"{class_name}.java")
#             with open(file_name, "w") as file:
#                 file.write(code)

#             # Compile the Java code
#             compile_result = subprocess.run(
#                 [javac_path, file_name],
#                 capture_output=True,
#                 text=True
#             )
#             if compile_result.returncode != 0:
#                 os.remove(file_name)  # Cleanup source file on error
#                 return jsonify({"error": compile_result.stderr.strip()})

#             # Run the Java code
#             result = subprocess.run(
#                 [java_path, "-cp", temp_dir, class_name],
#                 input=user_input,
#                 capture_output=True,
#                 text=True,
#                 timeout=10
#             )

#             # Cleanup files
#             os.remove(file_name)
#             os.remove(os.path.join(temp_dir, f"{class_name}.class"))

#             return jsonify({"output": result.stdout.strip(), "error": result.stderr.strip()})
#         else:
#             return jsonify({"error": f"Unsupported language: {language}"})
        
#         # Return the output or error
#         if result.returncode == 0:
#             return jsonify({"output": result.stdout.strip()})
#         else:
#             return jsonify({"error": result.stderr.strip()})
    
#     except KeyError as e:
#         return jsonify({"error": f"KeyError: {str(e)}"})
    
#     except subprocess.CalledProcessError as e:
#         return jsonify({"error": f"CalledProcessError: {str(e)}"})
    
#     except subprocess.TimeoutExpired as e:
#         return jsonify({"error": f"TimeoutExpired: {str(e)}"})
    
#     except Exception as e:
#         return jsonify({"error": f"Exception: {str(e)}"})



# #============================================Submit code runs here============================================
# @app.route("/check_code", methods=["POST"])
# def check_code():
#     try:
#         data = request.json
#         code = data["code"]
#         language = data["language"]
#         logging.info(f"Received code for language: {language}")

#         contest = collection2.find_one({})
#         if not contest:
#             logging.error("No contest found in collection2")
#             return jsonify({"error": "No contest found"})

#         psno = contest.get('psno')
#         if psno is None:
#             logging.error("No psno found in contest")
#             return jsonify({"error": "No psno found in contest"})

#         logging.info(f"psno: {psno}")

#         problem = collection.find_one({'psno': psno})
#         if not problem:
#             logging.error(f"No problem found with psno: {psno}")
#             return jsonify({"error": f"No problem found with psno: {psno}"})

#         logging.info(f"Problem statement: {problem.get('problem_statement', 'No problem statement available')}")

#         test_cases = problem.get("test_cases", [])
#         if not test_cases:
#             logging.error(f"No test cases found for problem with psno: {psno}")
#             return jsonify({"error": f"No test cases found for problem with psno: {psno}"})

#         results = []
#         all_passed = True
#         score = 0
    
#         if language == "python":
#             for index, test_case in enumerate(test_cases, start=1):
#                 cus_input = test_case.get("input", "").strip()
#                 logging.info(f"The Custom input fetched is : {cus_input} with data type{type(cus_input)}")
#                 expected_output = test_case.get("output", "").strip()
#                 logging.info(f"The Custom input fetched is : {expected_output} with data type{type(expected_output)}")
#                 logging.info(f'Test Case {index} - Input: {cus_input}, Expected Output: {expected_output}')
#                 result = execute_python(code, cus_input)
#                 actual_output = result["output"]
#                 logging.info(f"the actual output is {actual_output} with data type {type(actual_output)}")
#                 logging.info(f'This is the expected output {expected_output} with data type {type(expected_output)}')
#                 error_message = result.get("error", None)
#                 logging.info(f'This is the error {error_message}')
#                 if error_message:
#                     results.append(f"Test Case {index}: Failed. Error: {0}")
#                 elif str(actual_output) == str(expected_output):
#                     score += 10
#                     results.append(f"Test Case {index}: Passed")
#                 elif actual_output == expected_output:
#                     score += 10
#                     results.append(f"Test Case {index}: Passed")
#                 else:
#                     results.append(f"Test Case {index}: Failed. Got: '{actual_output}', Expected: '{expected_output}'")
#                     all_passed = False

#         elif language == "java":
#             for index, test_case in enumerate(test_cases, start=1):
#                 cus_input = test_case.get("input", "").strip()
#                 expected_output = test_case.get("output", "").strip()
#                 logging.info(f'Test Case {index} - Input: {cus_input}, Expected Output: {expected_output}')
#                 result = execute_java(code, cus_input)
#                 actual_output = result["output"]
#                 logging.info(f"the actual output is {actual_output} with data type {type(actual_output)}")
#                 logging.info(f'This is the expected output {expected_output} with data type {type(expected_output)}')
#                 error_message = result.get("error", None)
#                 error_message = result.get("error", None)
#                 # if error_message:
#                 #     results.append(f"Test Case {index}: Failed. Error: {0}")
#                 #     all_passed = False
#                 if actual_output == expected_output:
#                     score += 10
#                     results.append(f"Test Case {index}: Passed")
#                 elif str(actual_output) == str(expected_output):
#                     score += 10
#                     results.append(f"Test Case {index}: Passed")
#                 else:
#                     results.append(f"Test Case {index}: Failed. Got: '{actual_output}', Expected: '{expected_output}'")
#                     all_passed = False

#         else:
#             return jsonify({"error": f"Unsupported language: {language}"})

#         user_id = session.get('user', {}).get('user_id', 'anonymous')
#         if user_id != 'anonymous':
#             user_id = int(user_id)
        
#         store_score(user_id, score)
#         logging.info(f"Score: {score}, User: {session.get('user', 'anonymous')}")

#         response = {"results": results}
#         if all_passed:
#             session.pop('user', None)
#             response["redirect"] = "/login"
        
#         return jsonify(response)

#     except KeyError as e:
#         logging.error(f"KeyError: {str(e)}")
#         return jsonify({"error": f"KeyError: {str(e)}"})

#     except Exception as e:
#         logging.error(f"Exception: {str(e)}")
#         return jsonify({"error": f"Exception: {str(e)}"})


# #========================================================= Execute python =========================================================
# def execute_python(code, cus_input):
#     temp_filename = None
#     user_id = session.get('user', {}).get('user_id', 'anonymous')
#     logging.debug(f'Code to execute: {code}')
#     logging.info(f'This is the test case custom :{cus_input}')
#     try:
#         # Create a temporary file for the Python code
#         with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
#             temp_filename = temp_file.name
#             temp_file.write(code.encode('utf-8'))

#         process = subprocess.Popen(
#             ['python', temp_filename],
#             stdin=subprocess.PIPE,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )

#         stdout, stderr = process.communicate(input=cus_input)
#         # return {"output": stdout.strip(), "error": stderr.strip() if stderr else None}
#         return {"output": stdout.strip()}

#     except subprocess.CalledProcessError as e:
#         return {"error": f"CalledProcessError: {str(e)}"}

#     except subprocess.TimeoutExpired as e:
#         return {"error": f"TimeoutExpired: {str(e)}"}

#     except Exception as e:
#         return {"error": f"Exception: {str(e)}"}

#     finally:
#         file_uploaded = False
#         if temp_filename and os.path.exists(temp_filename) and file_uploaded==False:
#             try:
#                 new_filename = f"{user_id}.py" if user_id != 'anonymous' else "anonymous.py"
#                 sanitized_filename = sanitize_filename(new_filename)

#                 os.rename(temp_filename, sanitized_filename)

#                 with open(sanitized_filename, "rb") as file_stream:
#                     file_url = upload_code(file_stream, sanitized_filename)
#                     logging.info(f"File uploaded to: {file_url}")
#                     file_uploaded = True

#             except Exception as e:
#                 logging.error(f"Error during file upload: {str(e)}")

#             finally:
#                 if os.path.exists(sanitized_filename):
#                     os.remove(sanitized_filename)


# #========================================================= Execute Java =========================================================
# def execute_java(code, cus_input):
#     java_filename = None
#     class_filename = None
#     temp_dir = tempfile.gettempdir()
#     logging.debug(f'This is working directory: {temp_dir}')
    
#     try:
#         # Determine the Java class name
#         class_name = get_java_class_name(code)

#         if not class_name:
#             return {"output": "", "error": "Unable to determine the class name from the Java code."}

#         class_filename = os.path.join(temp_dir, f"{class_name}.class")
#         java_filename = os.path.join(temp_dir, f"{class_name}.java")
        
#         logging.info(f'The class file is stored: {class_filename}')
#         logging.info(f'The class file is stored: {java_filename}')
        
#         with open(java_filename, "w") as file:
#             file.write(code)

#         compile_command = ["javac", java_filename]
#         compile_process = subprocess.Popen(
#             compile_command,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )
#         compile_stdout, compile_stderr = compile_process.communicate()

#         if compile_process.returncode != 0:
#             return {"output": "", "error": f"Compilation Error: {compile_stderr.strip()}"}

#         execution_command = ["java", class_name]
#         execution_process = subprocess.Popen(
#             execution_command,
#             stdin=subprocess.PIPE,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )
#         execution_stdout, execution_stderr = execution_process.communicate(input=cus_input)

#         # return {"output": execution_stdout.strip(), "error": execution_stderr.strip() if execution_stderr else None}
#         return {"output": execution_stdout.strip()}

#     except subprocess.CalledProcessError as e:
#         return {"output": "", "error": f"CalledProcessError: {str(e)}"}

#     except subprocess.TimeoutExpired as e:
#         return {"output": "", "error": f"TimeoutExpired: {str(e)}"}

#     except Exception as e:
#         return {"output": "", "error": f"Exception: {str(e)}"}

#     finally:
#         user_id = session.get('user', {}).get('user_id', 'anonymous')
#         if java_filename and os.path.exists(java_filename):
#             try:
#                 new_filename = f"{user_id}.java" if user_id != 'anonymous' else "anonymous.java"
#                 sanitized_filename = sanitize_filename(new_filename)

#                 os.rename(java_filename, sanitized_filename)

#                 with open(sanitized_filename, "rb") as file_stream:
#                     file_url = upload_code(file_stream, sanitized_filename)
#                     logging.info(f"File uploaded to: {file_url}")

#             except Exception as e:
#                 logging.error(f"Error during file upload: {str(e)}")

#             finally:
#                 if os.path.exists(sanitized_filename):
#                     os.remove(sanitized_filename)

#         if class_filename and os.path.exists(class_filename):
#             try:
#                 new_filename = f"{user_id}.class" if user_id != 'anonymous' else "anonymous.class"
#                 sanitized_filename = sanitize_filename(new_filename)

#                 os.rename(class_filename, sanitized_filename)

#                 with open(sanitized_filename, "rb") as file_stream:
#                     file_url = upload_code(file_stream, sanitized_filename)
#                     logging.info(f"File uploaded to: {file_url}")

#             except Exception as e:
#                 logging.error(f"Error during file upload: {str(e)}")

#             finally:
#                 if os.path.exists(sanitized_filename):
#                     os.remove(sanitized_filename)
# file updated at 2025-03-09

# file updated at 2024-09-30

# file updated at 2024-11-27

# file updated at 2024-11-30

# file updated at 2024-12-14

# file updated at 2024-12-16

# file updated at 2025-01-29
