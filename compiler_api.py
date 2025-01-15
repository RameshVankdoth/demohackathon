import logging
import os
import re

import pymongo
import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG, filename="combined_execution.log")

load_dotenv()

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


client = pymongo.MongoClient(os.environ.get("MONGODB_URI"))
db = client[os.environ.get("MONGODB_PROBLEMS_DB")]
collection = db[os.environ.get("MONGODB_PROBLEMS_COLLECTION")]

document = collection.find_one({'psno': 11})
test_cases = document.get("test_cases", [])
score = 0
# OneCompiler API details
API_URL = "https://onecompiler-apis.p.rapidapi.com/api/v1/run"
HEADERS = {
    "x-rapidapi-key": "45f2a7db9cmsh4284c930ed09c24p1ca7b4jsn10ee469de6e2",
    "x-rapidapi-host": "onecompiler-apis.p.rapidapi.com",
    "Content-Type": "application/json"
}

def get_python_function(python_code):
    pattern = r'\bdef\s+(\w+)' 
    match = re.search(pattern, python_code)
    return match.group(1) if match else None

#Get the class name from the java code for compilation
def get_class(java_code):
    pattern = r'\bpublic\s+class\s+(\w+)'
    match = re.search(pattern, java_code)
    return match.group(1) if match else None

#Send the code to the API 
def run_code(language, content, file_name):
    payload = {
        "language": language,
        "stdin": "",
        "files": [{"name": file_name, "content": content}]
    }
    response = requests.post(API_URL, json=payload, headers=HEADERS)
    if response.status_code == 200:
        logging.info(f"{language.capitalize()} Response received")
        output = response.json()
        logging.info(response.json())
        logging.info(f"The output is {output['stdout']}")
        return response.json()

    else:
        logging.error(f"Error: {response.status_code}, {response.text}")
        return None


#This is python code request
def run_python_code():
    code = """
def count(number):
    original_number = number
    count = 0
    counted_digits = set()  # To track digits that have already been counted

    while number > 0:
        digit = number % 10  # Get the last digit
        number = number // 10  # Remove the last digit

        # Check if the digit is non-zero and hasn't been counted yet
        if digit != 0 and digit not in counted_digits:
            counted_digits.add(digit)  # Mark this digit as counted
            if original_number % digit == 0:  # Check if it divides evenly
                count += 1

    return count
""" 
    function_name = get_python_function(code)  # Extract function name (e.g., 'count')
    
    content = f"{code}\n\n"
    content += f"test_cases = {test_cases}\n\n"
    content += f"""
# Running test cases
for case in test_cases:
    input_value = case['input']
    expected_output = case['output']
    result = {function_name}(input_value)
    print(result)
"""
    logging.info(content)
    return run_code("python", content, "count_digits.py")



#Send the code for JAVA
def run_java_code():
    java_code = f"""
{java_headers}
"""
    java_code+="""

    public static int count(int number) {
        int originalNumber = number;
        int count = 0;
        Set<Integer> countedDigits = new HashSet<>();

        while (number > 0) {
            int digit = number % 10;
            number = number / 10;

            if (digit != 0 && !countedDigits.contains(digit)) {
                countedDigits.add(digit);
                if (originalNumber % digit == 0) {
                    count++;
                }
            }
        }
        return count;
    }
"""

    java_code += f"""
    public static void main(String[] args) {{
        Object[][] testCases = {{
            {",".join([f"{{{test_case['input']}, {test_case['output']}}}" for test_case in test_cases])}
        }};
        
        for (Object[] testCase : testCases) {{
            int inputValue = (int) testCase[0];
            int expectedOutput = (int) testCase[1];

            int result = {get_class(java_code)}.count(inputValue);
            System.out.println(result);
        }}
    }}
"""
    java_code+="""
    }
    """
    logging.info(f'Code is {java_code}')

    run_code("java",java_code,"Main.java")

python_response = run_python_code()
if python_response:
    logging.info(f"Python Output: {python_response}")

java_response = run_java_code()
if java_response:
    logging.info(f"Java Output: {java_response}")


# file updated at 2025-01-03

# file updated at 2024-08-04

# file updated at 2024-08-28

# file updated at 2024-09-29

# file updated at 2024-10-05

# file updated at 2024-11-13

# file updated at 2024-12-28

# file updated at 2025-01-05

# file updated at 2025-01-15
