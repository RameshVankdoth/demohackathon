import io
import os
import random
import re
import smtplib
import ssl
import string
import subprocess
import tempfile
import traceback
from datetime import datetime

import pyodbc
from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient
from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session, url_for)
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="templates")
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx'}
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY", "6a38d4e553910d47fcc908422f50591abfec0d131db734a5691aacb23e44be4"
)  # Use environment variable for secret key

AZURE_CONNECTION_STRING  = 'DefaultEndpointsProtocol=https;AccountName=artisetdata;AccountKey=pnBke+Pj1bvkaipv2aOgH6vsfFQfm3JS29szjhx2zQHqdWnKf/t7sptSJ0XVKRTYlmQgvwzkoNnX+ASta8kGdg==;EndpointSuffix=core.windows.net'  # Replace with your Azure Storage connection string
RESUME_CONTAINER_NAME  = 'resumestorage' 
CODE_CONTAINER_NAME  = 'codestorage' 


blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client_resume = blob_service_client.get_container_client(RESUME_CONTAINER_NAME)
container_client_code = blob_service_client.get_container_client(CODE_CONTAINER_NAME)

psno = 0

def sanitize_filename(filename):
    return re.sub(r'[^\w\-.]', '', filename).strip()

def upload_to_blob(file_stream, filename):
    try:
        filename = sanitize_filename(filename)
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=RESUME_CONTAINER_NAME, blob=filename)
        blob_client.upload_blob(file_stream, blob_type="BlockBlob", overwrite=True)
        return blob_client.url
    except Exception as e:
        print(f"Error uploading to Azure Blob: {str(e)}")
        raise

def upload_code(file_stream, filename):
    try:
        filename = sanitize_filename(filename)
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=CODE_CONTAINER_NAME, blob=filename)
        blob_client.upload_blob(file_stream, blob_type="BlockBlob", overwrite=True)
        return blob_client.url
    except Exception as e:
        print(f"Error uploading to Azure Blob: {str(e)}")
        raise

# Email configuration
smtp_port = 587
smtp_server = "smtp.gmail.com"
email_from = "vijay.artiset1@gmail.com"
pswd = "qtbhggrdbquptsls"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_otp(length=6):
    return ''.join(random.choice(string.digits) for _ in range(length))

# MongoDB setup
client = MongoClient(
    "mongodb+srv://vankyrs:rukHnjdLGabqQGnA@problestatement.ztrbltk.mongodb.net/?retryWrites=true&w=majority&appName=ProbleStatement"
)

#MonngoDB for Problem Statements
db = client["Problems"]
collection = db["Statements"]

#MongoDB for contest Details 
db2 = client["Contest"]
collection2 = db2["Contests"]

# SQL Server setup
connection_string = (
    'Driver={ODBC Driver 17 for SQL Server};Server=tcp:hackathondatabase.database.windows.net,1433;Database=hachathon;Uid=hackathon-admin;Pwd={Pune@2024};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
)

contests = collection2.find_one({})
psno = contests['psno']
problems = list(collection.find_one({}))


#Functions without any kind of routes enabled
def get_connection():
    return pyodbc.connect(connection_string)


def get_java_class_name(code):
    match = re.search(r'\bpublic\s+class\s+(\w+)', code)
    if match:
        return match.group(1)
    return None


#Route for main landing page no login included 
@app.route("/")
@app.route("/home")
def home():
    
    contests = list(collection2.find({}))
    return render_template("landingpage.html", contests=contests)


# Route for login form
@app.route("/login")
def login():
    return render_template("login.html")


@app.route('/resetpass')
def resetpass():
    return render_template('resetpass.html')


@app.route("/loginpage", methods=["POST", "GET"])
def loginpage():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Use parameterized query to avoid SQL injection
            cursor.execute("SELECT * FROM Student WHERE EmailId = ?", (email,))
            user = cursor.fetchone()

            if user and check_password_hash(user[5], password):
                # Check if the user has already taken the test
                cursor.execute("SELECT * FROM Evaluation WHERE StudentID = ?", (user[0],))
                evals = cursor.fetchall()

                if evals:
                    flash("You have already taken this test.")
                    return redirect(url_for("loginpage"))
                else:
                    # Store user data in session
                    session["user"] = {
                        "user_id":user[0],
                        "fname": user[1],
                        "lname": user[3],
                        "email": user[9],
                        "college": user[14],
                        "mobile": user[10]
                    }

                    # Redirect to the contest page
                    return redirect(url_for("code"))  # Pass parameters if needed

            else:
                flash("Invalid email or password. Please try again.")
                return redirect(url_for("loginpage"))

        except Exception as e:
            flash(f"An error occurred: {str(e)}")
            return redirect(url_for("loginpage"))

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    return render_template("login.html")


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



@app.route("/code")
def code():
    if "user" in session:
        try:
            contests = collection2.find_one({})
            psno = contests['psno']
            
            # Fetch the specific problem using psno
            problem = collection.find({})[psno]  # Modify this query as per your database schema
            print(problem)
            if problem:
                return render_template("index.html", user=session["user"], problem=problem, contests=contests)
            else:
                flash("Problem not found.")
                return render_template("index.html", user=session["user"], problem=None)
        
        except Exception as e:
            flash(f"An error occurred: {str(e)}")
            return render_template("index.html", user=session["user"], problem=None)
    
    else:
        flash("You are not logged in.")
        return redirect(url_for("login"))


@app.route("/contestreg")
def contestreg():
    return render_template("contestreg.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        try:
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
                return redirect(url_for("register"))

            # Validate if all necessary fields are present
            if not all([fullname, email, mobile, gender, dob, education_level, college, marks, course, specialization, primary_skill, secondary_skill, home_state, home_city, current_state, current_city, preferred_location]):
                flash("Please fill in all required fields.")
                return redirect(url_for("register"))

            # Handle file upload
            if 'resume' not in request.files:
                flash('No resume file found.')
                return redirect(url_for('register'))

            file = request.files['resume']
            if file.filename == '':
                flash('No selected file')
                return redirect(url_for('register'))

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_stream = io.BytesIO(file.read())
                resume_url = upload_to_blob(file_stream, filename)
            else:
                flash('Invalid file type')
                return redirect(url_for('register'))

            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT EmailId, Mobile FROM Student WHERE EmailId = ? OR Mobile = ?",
                    (email, mobile),
                )
                existing_user = cursor.fetchone()
                if existing_user:
                    flash("You are already registered with this email or mobile number.")
                    return redirect(url_for("register"))

                cursor.execute("SELECT state_id, state_name FROM states")
                states = cursor.fetchall()
                
                cursor.execute("SELECT city_id, city_name, state_id FROM cities")
                cities = cursor.fetchall()

                cursor.execute(
                    "INSERT INTO Student (Fullname, Fname, Mname, Lname, Password, EmailId, Mobile, Gender, DOB, EducationLevel, College, Marks, Course, Specialization, PrimarySkill, SecondarySkill, PositionApplying, AlternateMobile, AlternateEmail, HomeState, HomeCity, CurrentState, CurrentCity, PreferredLocation, DOE, ResumeFilePath) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (fullname, fname, mname_str, lname, password_hash, email, mobile, gender, dob, education_level, college, marks, course, specialization, primary_skill, secondary_skill,
                     position_applying, alternate_mobile, alternate_email, states[home_state-1][1], cities[home_city-1][1], states[current_state-1][1], cities[current_city-1][1], preferred_location, doe, resume_url)
                )
               
                conn.commit()
                flash("Registration successful")
                return redirect(url_for("thankyou"))

        except Exception as e:
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
    except Exception as e:
        print(f"Database error: {e}")
        flash("An error occurred while fetching form data.")
        return render_template("registration.html")

    return render_template("registration.html", skills=skills, courses=courses, levels=levels, cities=cities_list, states=states_list, positions=positions)


@app.route("/get_cities")
def get_cities():
    state_id = request.args.get("state_id", type=int)
    if (state_id is None):
        return jsonify({"cities": []})

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT city_id, city_name FROM cities WHERE state_id = ?", (state_id,))
            cities = cursor.fetchall()
            cities_list = [{"id": city[0], "name": city[1]} for city in cities]

    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"cities": []})

    return jsonify({"cities": cities_list})



# # Logout section to close the user sessions
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# #Not te be changed, any changes will affect the working of code editor and will not show any output.

def store_score(user_id, score):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Convert user_id to integer if it's not 'anonymous'
            if user_id == 'anonymous':
                # Handle the 'anonymous' case, e.g., skip scoring or use a default value
                print("Anonymous user detected; no score stored.")
                return

            user_id = int(user_id)  # Convert to integer if not 'anonymous'

            # Fetch all student IDs from the Evaluation table
            cursor.execute("SELECT StudentID FROM Evaluation")
            existing_ids = [row[0] for row in cursor.fetchall()]  # Fetch all rows and get the first column
            
            # Check if the user_id already exists
            if user_id in existing_ids:
                flash("You have already given this test.")
                return  # Exit the function if the user has already taken the test
            
            # Insert the new score
            cursor.execute("INSERT INTO Evaluation (StudentID, Marks) VALUES (?, ?)",
                           (user_id, score))
            conn.commit()  # Commit the transaction to save changes

    except Exception as e:
        # Print the exception or use logging for better error handling
        print(f"Database error: {e}")



@app.route("/execute_code", methods=["POST"])
def execute_code():
    try:
        data = request.json
        code = data["code"]
        print(code)
        language = data["language"]
        user_input = data.get("input", "")
        print(user_input)
        if language == "python":
            # Write code to a temporary Python file
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
                temp_file.write(code.encode())
                temp_file.flush()  # Ensure all data is written to file
                temp_file_name = temp_file.name
                for i in temp_file:
                    print(i)
            # Execute the temporary Python file
            result = subprocess.run(
                ["python", temp_file_name],
                input=user_input,
                capture_output=True,
                text=True,
                timeout=25,
                shell=True
            )

            # Clean up temporary file
            os.remove(temp_file_name)
        
        elif language == "java":
            # Java execution remains unchanged from your original code
            class_name = get_java_class_name(code)  # Implement this function
            if not class_name:
                return jsonify({"error": "Unable to determine the class name from the Java code."})
            
            file_name = f"{class_name}.java"
            with open(file_name, "w") as file:
                file.write(code)
            
            compile_result = subprocess.run(
                ["javac", file_name],
                capture_output=True,
                text=True
            )
            if compile_result.returncode != 0:
                return jsonify({"error": compile_result.stderr.strip()})
            
            result = subprocess.run(
                ["java", class_name],
                input=user_input,
                capture_output=True,
                text=True,
                timeout=10,
                shell=False
            )
            os.remove(f"{class_name}.class")
            os.remove(file_name)
        
        else:
            return jsonify({"error": f"Unsupported language: {language}"})
        
        if result.returncode == 0:
            return jsonify({"output": result.stdout.strip()})
        else:
            return jsonify({"error": result.stderr.strip()})
    
    except KeyError as e:
        return jsonify({"error": f"KeyError: {str(e)}"})
    
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"CalledProcessError: {str(e)}"})
    
    except subprocess.TimeoutExpired as e:
        return jsonify({"error": f"TimeoutExpired: {str(e)}"})
    
    except Exception as e:
        return jsonify({"error": f"Exception: {str(e)}"})


@app.route("/check_code", methods=["POST"])
def check_code():
    try:
        data = request.json
        code = data["code"]
        language = data["language"]
        # Log incoming code and language
        app.logger.info(f"Received code for language: {language}")

        # Fetch psno from the contest collection
        contest = collection2.find_one({})
        if not contest:
            app.logger.error("No contest found in collection2")
            return jsonify({"error": "No contest found"})

        psno = contest.get('psno')
        if psno is None:
            app.logger.error("No psno found in contest")
            return jsonify({"error": "No psno found in contest"})

        app.logger.info(f"psno: {psno}")

        # Fetch the specific problem using psno from the statements collection
        problem = collection.find()[psno]
        if not problem:
            app.logger.error(f"No problem found with psno: {psno}")
            return jsonify({"error": f"No problem found with psno: {psno}"})

        # Log the problem details
        app.logger.info(f"Problem statement: {problem.get('problem_statement', 'No problem statement available')}")

        test_cases = problem.get("test_cases", [])
        print(test_cases)
        if not test_cases:
            app.logger.error(f"No test cases found for problem with psno: {psno}")
            return jsonify({"error": f"No test cases found for problem with psno: {psno}"})

        results = []
        all_passed = True
        score = 0
        if language == "python":
            for index, test_case in enumerate(test_cases, start=1):
                cus_input = test_case.get("input", "").strip()
                expected_output = test_case.get("output", "").strip()
                result = execute_python(code, cus_input)
                actual_output = result["output"]
                error_message = result.get("error", None)

                if error_message:
                    results.append(f"Test Case {index}: Failed. Error: {error_message}")
                    all_passed = False
                elif actual_output == expected_output:
                    score+=10
                    results.append(f"Test Case {index}: Passed")
                else:
                    score+=0
                    results.append(f"Test Case {index}: Failed. Got: '{actual_output}', Expected: '{expected_output}'")
                    all_passed = False

        elif language == "java":
            for index, test_case in enumerate(test_cases, start=1):
                cus_input = test_case.get("input", "").strip()
                expected_output = test_case.get("output", "").strip()
                result = execute_java(code, cus_input)
                actual_output = result["output"]
                error_message = result.get("error", None)

                if error_message:
                    results.append(f"Test Case {index}: Failed. Error: {error_message}")
                    all_passed = False
                elif actual_output == expected_output:
                    score+=10
                    results.append(f"Test Case {index}: Passed")
                else:
                    score+=0
                    results.append(f"Test Case {index}: Failed. Got: '{actual_output}', Expected: '{expected_output}'")
                    all_passed = False

        else:
            return jsonify({"error": f"Unsupported language: {language}"})

        user_id = session.get('user', {}).get('user_id', 'anonymous')
        
        # Ensure user_id is an integer if not 'anonymous'
        if user_id != 'anonymous':
            user_id = int(user_id)
        
        store_score(user_id, score)
        
        # Log score and user
        app.logger.info(f"Score: {score}, User: {session.get('user', 'anonymous')}")
        
        response = {"results": results}
        if all_passed:
            session.pop()
            response["redirect"] = "/login"
        return jsonify(response)

    except KeyError as e:
        app.logger.error(f"KeyError: {str(e)}")
        return jsonify({"error": f"KeyError: {str(e)}"})

    except Exception as e:
        app.logger.error(f"Exception: {str(e)}")
        return jsonify({"error": f"Exception: {str(e)}"})


def execute_python(code, cus_input):
    temp_filename = None
    user_id = session.get('user', {}).get('user_id', 'anonymous')
    
    try:
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
            temp_filename = temp_file.name
            temp_file.write(code.encode())

        # Construct the command to run the Python script
        command = f"python {temp_filename}"

        # Run the command in a new shell environment
        result = subprocess.run(
            command, input=cus_input, capture_output=True, text=True, timeout=5, shell=True
        )

        output = result.stdout.strip()
        error = result.stderr.strip() if result.stderr else None

        return {"output": output, "error": error}

    except subprocess.CalledProcessError as e:
        return {"error": f"CalledProcessError: {str(e)}"}

    except subprocess.TimeoutExpired as e:
        return {"error": f"TimeoutExpired: {str(e)}"}

    except Exception as e:
        return {"error": f"Exception: {str(e)}"}

    finally:
        if temp_filename and os.path.exists(temp_filename):
            try:
                # Rename the temporary file to include user_id if not 'anonymous'
                new_filename = f"{user_id}.py" if user_id != 'anonymous' else "anonymous.py"
                sanitized_filename = sanitize_filename(new_filename)

                # Rename the temporary file
                os.rename(temp_filename, sanitized_filename)

                # Open the renamed file for reading
                with open(sanitized_filename, "rb") as file_stream:
                    # Upload to Azure Blob Storage
                    file_url = upload_code(file_stream, sanitized_filename)
                    print(f"File uploaded to: {file_url}")

            except Exception as e:
                print(f"Error during file upload: {str(e)}")

            finally:
                # Clean up local files
                if os.path.exists(sanitized_filename):
                    os.remove(sanitized_filename)

def execute_java(code, cus_input):
    java_filename = None
    class_filename = None
    try:
        class_name = get_java_class_name(code)  # Define this function

        if not class_name:
            return {"output": "", "error": "Unable to determine the class name from the Java code."}

        java_filename = f"{class_name}.java"
        class_filename = f"{class_name}.class"

        with open(java_filename, "w") as file:
            file.write(code)

        compile_command = ["javac", java_filename]
        compile_result = subprocess.run(
            compile_command, capture_output=True, text=True, timeout=5, shell=False
        )

        if compile_result.returncode != 0:
            return {"output": "", "error": f"Compilation Error: {compile_result.stderr.strip()}"}

        execution_command = ["java", class_name]
        result = subprocess.run(
            execution_command, input=cus_input, capture_output=True, text=True, timeout=5, shell=False
        )

        output = result.stdout.strip()
        error = result.stderr.strip() if result.stderr else None

        return {"output": output, "error": error}

    except subprocess.CalledProcessError as e:
        return {"output": "", "error": f"CalledProcessError: {str(e)}"}

    except subprocess.TimeoutExpired as e:
        return {"output": "", "error": f"TimeoutExpired: {str(e)}"}

    except Exception as e:
        return {"output": "", "error": f"Exception: {str(e)}"}

    finally:
        user_id = session.get('user', {}).get('user_id', 'anonymous')
        if java_filename and os.path.exists(java_filename):
            try:
                # Rename the temporary file to include user_id if not 'anonymous'
                new_filename = f"{user_id}.py" if user_id != 'anonymous' else "anonymous.java"
                sanitized_filename = sanitize_filename(new_filename)

                # Rename the temporary file
                os.rename(java_filename, sanitized_filename)

                # Open the renamed file for reading
                with open(sanitized_filename, "rb") as file_stream:
                    # Upload to Azure Blob Storage
                    file_url = upload_code(file_stream, sanitized_filename)
                    print(f"File uploaded to: {file_url}")

            except Exception as e:
                print(f"Error during file upload: {str(e)}")

            finally:
                # Clean up local files
                if os.path.exists(sanitized_filename):
                    os.remove(sanitized_filename)

        if class_filename and os.path.exists(class_filename):
            try:
                # Rename the temporary file to include user_id if not 'anonymous'
                new_filename = f"{user_id}.py" if user_id != 'anonymous' else "anonymous.java"
                sanitized_filename = sanitize_filename(new_filename)

                # Rename the temporary file
                os.rename(class_filename, sanitized_filename)

                # Open the renamed file for reading
                with open(sanitized_filename, "rb") as file_stream:
                    # Upload to Azure Blob Storage
                    file_url = upload_code(file_stream, sanitized_filename)
                    print(f"File uploaded to: {file_url}")

            except Exception as e:
                print(f"Error during file upload: {str(e)}")

            finally:
                # Clean up local files
                if os.path.exists(sanitized_filename):
                    os.remove(sanitized_filename)
        
#Password validation fro vijay

@app.route('/send_otp', methods=['POST'])
def send_otp():
    email_to = request.form['email']  # To be checked in the backend if exists go ahead else warning
    try:
        conn = get_connection()  # Assuming get_connection() retrieves your SQL Server connection
        cursor = conn.cursor()

        # Use parameterized query to avoid SQL injection
        cursor.execute("SELECT * FROM Students WHERE EmailId = ?", (email_to,))
        user = cursor.fetchone()
        if user:
            # Store user data in session
            otp = generate_otp()
            session['otp'] = otp
            session['user_email'] = email_to
            session['password'] = user[5]
            session['pass1'] = user[6]
            session['pass2'] = user[7]
            session['pass3'] = user[8]

            if all(session.get('pass1'), session.get('pass2'), session.get('pass3')):
                flash("You have reached the password reset limit, please contact Artiset.")
                return redirect(url_for('resetpass'))

            message = f"Subject: Your OTP Code\n\nDear User,\n\nYour OTP code is: {otp}\n\nPlease use this code to complete your verification.\n\nBest regards,\nArtiset Team"

            try:
                context = ssl.create_default_context()
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls(context=context)
                    server.login(email_from, pswd)
                    server.sendmail(email_from, email_to, message)
                flash("OTP sent successfully to your email ID.", "success")
            except smtplib.SMTPException as e:
                print(f"SMTP error: {e}")
                flash("Failed to send OTP. Please check the email address and try again.", "error")
        else:
            flash("Email address not found. Please check and try again.", "warning")
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        flash("Database error. Please try again later.", "error")
    except Exception as e:
        print(f"General error: {e}")
        flash("An unexpected error occurred. Please try again later.", "error")
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('resetpass'))

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    user_otp = request.form['otp']
    if 'otp' in session and user_otp == session['otp']:
        flash("OTP verified successfully.", "success")
        session.pop('otp', None)
        return redirect(url_for('setpass'))
    else:
        flash("Invalid OTP. Please try again.", "error")
        return redirect(url_for('resetpass'))

@app.route('/setpass', methods=['GET'])
def setpass():
    if 'user_email' in session:
        return render_template('setpass.html')
    else:
        flash('Session expired. Please try again.')
        return redirect(url_for('resetpass'))

@app.route('/update_password', methods=['POST'])
def update_password():
    if 'user_email' not in session:
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
        flash('Passwords do not match.')
        return redirect(url_for('setpass'))

    password_hash = generate_password_hash(new_password)
    
    # Check for password reset history
    if pass1 and pass2 and pass3:
        flash('You have reached the password reset limit. Please contact Artiset.')
        return redirect(url_for('setpass'))

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Update the password and shift the history
        cursor.execute("UPDATE Students SET Password = ?, respass3 = respass2, respass2 = respass1, respass1 = ? WHERE EmailId = ?", (password_hash, password, email))
        conn.commit()

        flash('Password updated successfully.')
        session.pop('user_email', None)
        return redirect(url_for('login'))
    except pyodbc.Error as e:
        flash(f"Database error occurred: {str(e)}")
        return redirect(url_for('setpass'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}")
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
    app.run(debug=True, port=5000)
    