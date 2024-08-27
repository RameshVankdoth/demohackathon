import os
import subprocess
import tempfile

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# MongoDB Client`
client = MongoClient(os.environ.get("MONGODB_URI"))

def fetch_input_from_mongodb(i):
    try:
        # Connect to MongoDB
        db = client[os.environ.get("MONGODB_PROBLEMS_DB")]
        collection = db[os.environ.get("MONGODB_PROBLEMS_COLLECTION")]
        
        # Fetch the document
        document = collection.find_one()  # Adjust query as needed
        if document is None:
            raise ValueError("No document found in the collection.")
        
        # Extract the first test case's input data
        test_cases = document.get('test_cases', [])
        if not test_cases:
            raise ValueError("No test cases found in the document.")
        
        input_data = test_cases[i].get('input', '')
        if not input_data:
            raise ValueError("No input data found in the test case.")
        
        return input_data
    except Exception as e:
        print(f"Error fetching data from MongoDB: {e}")
        raise

def write_code_to_temp_file(code):
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(code.encode('utf-8'))
            temp_filename = temp_file.name
        
        return temp_filename
    except Exception as e:
        print(f"Error writing code to temporary file: {e}")
        raise

def run_python_script(temp_filename, input_data):
    try:
        # Run the temporary Python script
        process = subprocess.Popen(
            ['python', temp_filename],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send the input data to the script
        stdout, stderr = process.communicate(input=input_data)
        
        return stdout, stderr
    except Exception as e:
        print(f"Error running Python script: {e}")
        raise
    finally:
        # Clean up temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

def main():
    try:
        # Fetch input data from MongoDB
        for i in range(5):
            input_data = fetch_input_from_mongodb(i)
            print(f"Fetched input data: {input_data}")  # Debug print
        
            # Python code to be executed (this should be received from the frontend)
            python_code = '''import sys

def length_of_last_word(s):
    # Trim leading and trailing spaces
    s = s.strip()
    # Split the string into words
    words = s.split()
    # Return the length of the last word
    if words:
        return len(words[-1])
    return 0

if __name__ == "__main__":
    input_str = sys.stdin.read().strip()
    if not input_str:
        print("Error: No input provided")
    else:
        print(length_of_last_word(input_str))
            '''
            
            # Write the Python code to a temporary file
            temp_filename = write_code_to_temp_file(python_code)
            print(f"Temporary file created: {temp_filename}")  # Debug print
            
            # Run the Python script with the input data
            stdout, stderr = run_python_script(temp_filename, input_data)
            
            # Print or handle the output and error
            print("Output:", stdout)
            if stderr:
                print("Error:", stderr)
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
