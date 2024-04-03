# ICT2214-Project
ICT2214 Web Security Project Group A01-G 15

# Website Vulnerability Assessment

# Username and Password Enumeration
To use these 2 features,we will use the login form to extract the usernames and passwords from the database. 
We will go to the login form using burpsuite to find the user and password parameter by entering a random username and password and submit on the login form.
<img width="407" alt="test3" src="https://github.com/ESLunarPhoenix/ICT2214-Project/assets/89129080/050a4225-ddf4-490d-8cee-d625040f003a">


# Database Enumeration
To start off, the user using NoSQL Bandit is able to choose an option from the tool menu, to perform database enumeration, the user will have to select option 3.
After option 3 is selected the tool will prompt the user to enter the MongoDB URL they wish to view the contents from.

<img width="407" alt="test3" src="https://github.com/ESLunarPhoenix/ICT2214-Project/assets/121931429/46483784-2646-45de-bffd-a2d3bc7d9b39">


Once the user enters the MongoDB URL, the tool will prompt the user to enter the ObjectID of the database field he/she wishes to view. The search query works by reading the ObjectID of the user input in the database, and displaying the relevant fields for the user to see.

<img width="407" alt="test2" src="https://github.com/ESLunarPhoenix/ICT2214-Project/assets/121931429/c598ed4e-9b57-4e08-98e2-5c35b8619db3">


The tool will now display the contents of the ObjectID. The figure below shows the field names “username”, and “password” from the MongoDB database. The user can get the relevant data from a specific ObjectID, and also view other data by searching other ObjectIDs. The tool will prompt the user to input a new ObjectID after displaying the fields of an ObjectID. 

<img width="407" alt="test" src="https://github.com/ESLunarPhoenix/ICT2214-Project/assets/121931429/4757a7a7-5e2d-4d3b-9c60-6d7628709aca">

# Database Fingerprinting





