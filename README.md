# ICT2214-Project Group-A01-G 15 - NoSQL Bandit

1. Download the nosql_bandit_MAIN.py file.

2. Run the tool using python 3. Python 3 can be downloaded from the official Python website here: [https://www.python.org/downloads/](url)
<img width="407" alt="python" src="https://github.com/ESLunarPhoenix/ICT2214-Project/assets/121931429/4d64f761-04c7-4b7e-84ba-260f18993bce">

3. The user will now be able to use the tool and select desired options from the toolkit menu.

# Website Vulnerability Assessment
In order to perform a website vulnerability assessment for nosql injection vulnerabilities, the user will first select option 5.
The user will then be given the option to test for login forms(option 1) or a url with GET parameters(option 2).
![image](https://github.com/ESLunarPhoenix/ICT2214-Project/assets/33411285/be50779d-af0f-498e-b87b-e2d8c69ff7f4)

The user will select option 1 to test for login forms. NoSQL Bandit will test if the username and password parameters in the login form is vulnerable to NoSQL injection attacks by injecting malicious payloads into it. It will then inform the user if the username and password parameters are vulnerable to NoSQL injection attacks as well as the malicious payload used to trigger the vulnerability. 
![image](https://github.com/ESLunarPhoenix/ICT2214-Project/assets/33411285/b48d0a73-0191-4416-9295-e421012b607e)

The user will select option 2 to test for a url with GET parameters. NoSQL Bandit will test if the GET parameter is vulnerable by injecting malcious payloads into it. It will then inform the user which payload the GET parameter is vulnerable or not vulnerable to.
![image](https://github.com/ESLunarPhoenix/ICT2214-Project/assets/33411285/ff2ccae9-aa40-4b8f-ab0b-30ee69d6cda6)

# Username and Password Enumeration
To use these 2 features,we will use the login form to extract the usernames and passwords from the database. 
We will access the login form using burpsuite to find the user and password parameter by entering a random username and password and submit on the login form.

<img width="407" src="https://github.com/ESLunarPhoenix/ICT2214-Project/assets/89129080/050a4225-ddf4-490d-8cee-d625040f003a">

After that, we will review the response text in burpsuite that indicated the failed login that we get from sending random username and password. In this example, the response text that indicates failed login is “Invalid username or password”.

<img width="407" src="https://github.com/ESLunarPhoenix/ICT2214-Project/assets/89129080/ff04db4b-f44f-4c87-8db7-7b26effd2162">

We will then use the username enumeration feature by selecting option 1 to extract the valid usernames from the database through the login form.

<img width="500" height="200" src="https://github.com/ESLunarPhoenix/ICT2214-Project/assets/89129080/c359574b-8511-4eef-8550-33408b5cb9c3">

<img width="407"  src="https://github.com/ESLunarPhoenix/ICT2214-Project/assets/89129080/b5b73dcd-e0ed-4a22-9ce6-c2b572af4b79">

Finally, we can use the password enumeration feature by selecting option 2 to extract the password of the specific username.

<img width="407" src="https://github.com/ESLunarPhoenix/ICT2214-Project/assets/89129080/f05c6b4e-1ebf-4354-98d8-610544b33d37">

# Database Enumeration
MongoDB URL and ObjectIDs inside the mongoDB_Enum.txt file can be used for testing this feature.

To start off, the user using NoSQL Bandit is able to choose an option from the tool menu, to perform database enumeration, the user will have to select option 3.
After option 3 is selected the tool will prompt the user to enter the MongoDB URL they wish to view the contents from.

<img width="407" alt="test3" src="https://github.com/ESLunarPhoenix/ICT2214-Project/assets/121931429/46483784-2646-45de-bffd-a2d3bc7d9b39">

Once the user enters the MongoDB URL, the tool will prompt the user to enter the ObjectID of the database field he/she wishes to view. The search query works by reading the ObjectID of the user input in the database, and displaying the relevant fields for the user to see.

<img width="407" alt="test2" src="https://github.com/ESLunarPhoenix/ICT2214-Project/assets/121931429/c598ed4e-9b57-4e08-98e2-5c35b8619db3">


The tool will now display the contents of the ObjectID. The figure below shows the field names “username”, and “password” from the MongoDB database. The user can get the relevant data from a specific ObjectID, and also view other data by searching other ObjectIDs. The tool will prompt the user to input a new ObjectID after displaying the fields of an ObjectID. 

<img width="407" alt="test" src="https://github.com/ESLunarPhoenix/ICT2214-Project/assets/121931429/4757a7a7-5e2d-4d3b-9c60-6d7628709aca">

# Database Fingerprinting
The user should select option 4 to execute the Database Fingerprinting.
Upon selecting option 4, the user will see a request to provide a URL such as the following:
![tool](https://github.com/ESLunarPhoenix/ICT2214-Project/assets/25898256/fe76de01-406d-45d7-bfa8-2c2e79c4a13a)

The user will need to go to the target website and locate a page that has GET parameters such as in the following image:
![portswig](https://github.com/ESLunarPhoenix/ICT2214-Project/assets/25898256/55682d37-9103-4d1f-9109-859bec680c54)

The user will then need to input this URL into the tool. The tool will then automatically attempt to fingerprint the database and provide an output at the end.
![Output](https://github.com/ESLunarPhoenix/ICT2214-Project/assets/25898256/3e6ca34c-f18c-4e5c-97db-c6d0ca3806c2)
