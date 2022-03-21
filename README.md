# hc_reimbursement
CS253 project:
Built a web app that will allow users to apply for reimbursement claims online by simply filling an online form and providing required details. The system would also help users view already submitted forms and their status. The HC staff can scrutinize and verify the applications. They can approve and send the details to the Accounts department or reject the claims and update the status of the form.

## Directory Structure  
.
├── README.md  
├── requirements.txt  
└── src  
    ├── db.sqlite3  
    ├── dummyData  
    │   ├── db.json  
    │   ├── readme.md  
    │   └── user_password.txt  
    ├── manage.py  
    ├── src  
    │   ├── asgi.py  
    │   ├── __init__.py  
    │   ├── settings.py  
    │   ├── urls.py  
    │   ├── views.py  
    │   └── wsgi.py  
    └── user  
        ├── admin.py  
        ├── apps.py  
        ├── __init__.py  
        ├── migrations  
        │   ├── 0001_initial.py  
        │   ├── __init__.py  
        ├── models.py  
        ├── static  
        │   ├── css  
        │   │   ├── bootstrap.css  
        │   │   ├── bootstrap.css.map  
        │   │   ├── bootstrap.min.css  
        │   │   ├── bootstrap.min.css.map  
        │   │   ├── bootstrap-theme.css  
        │   │   ├── bootstrap-theme.css.map  
        │   │   ├── bootstrap-theme.min.css  
        │   │   ├── bootstrap-theme.min.css.map   
        │   │   └── index.css  
        │   ├── fonts  
        │   │   ├── glyphicons-halflings-regular.eot  
        │   │   ├── glyphicons-halflings-regular.svg  
        │   │   ├── glyphicons-halflings-regular.ttf  
        │   │   ├── glyphicons-halflings-regular.woff  
        │   │   └── glyphicons-halflings-regular.woff2  
        │   └── js  
        │       ├── bootstrap.js  
        │       ├── bootstrap.min.js  
        │       ├── jquery-3.5.1.min.js  
        │       └── npm.js  
        ├── templates  
        │   ├── accounts_dashboard.html  
        │   ├── accounts_profile.html  
        │   ├── doctor_dashboard.html  
        │   ├── doctor_profile.html  
        │   ├── form.html  
        │   ├── hcadmin_dashboard.html  
        │   ├── hcadmin_profile.html  
        │   ├── index.html  
        │   ├── login.html  
        │   ├── patient_dashboard.html  
        │   ├── patient_profile.html  
        │   ├── signin.html  
        │   ├── signup_admin.html  
        │   └── signup.html  
        ├── tests.py  
        ├── urls.py  
        ├── utils.py  
        └── views.py  
   
### Description 
* ./manage.py- Script that helps with management of the site i.e. making migrations and running the server

* ./dummyData/db.json- Stores dummy data that can be loaded for testing the application

* ./db.sqlite3- Database in sqlite3, storing data in tables based on different models defined in model.py

* ./user/settings.py- Contains the configuration of our website, i.e. database settings, logging configuration and location of static files.

* ./user/model.py-  Stores all the models for our project i.e. an object which is stored in the database. The properties and methods for each object are defined in the class.

* ./user/admin.py-  Manages the Django admin interface by registering the models defined.

* ./user/views.py- Contains the main logic of the application which requests information from the models created and pass it to the template
 
* ./user/urls.py- All the paths for the views and to access the application are configured.

* ./user/templates- Contain the frontend files to present the site in HTML.

./static-  Static css and bootstrap files

## How to run ?(Key points)
* A virtual environment is create using the following command: ```python -m venv myvenv``` which needs to be activated using
  ```myvenv\Scripts\activate```
* The software requirements for the given application are installed using- ```pip install -r requirements.txt ``` which installs dependencies like django
* The database is created and the migrations are applied using: ``` python manage.py migrate```
* To login as admin, a superuser account is created which has control overall control of the site by running: 
        ```python manage.py createsuperuser```
* The web server is started by running: ```python manage.py runserver```


## To load some dummy data into the database
Run ```python3 manage.py loaddata dummyData/db.json``` from the ``src`` folder 

## Future Development Plans

* Update UI: Make changes in the UI to make the system more user friendly and fluid by providing intuitive animations and a uniform colour code to represent specific information without discrepancies.
* Useful Links: Provide a page with useful links related to HC. Provide a page with just info on Offline Reimbursement Plan.
Change Password Option: Allows the user to change the password by providing the current password, and then asking for the new password and its retype. This changes the user password in the database.
* Notification by Mail (whenever Status Change or Feedback received): Whenever the reimbursement status changes, the patient user who filled the form is automatically notified through their mail.
* Manage Notification: Provides the option to toggle the notifications ON or OFF, or even selectively enable the notifications.
* Provide a multiple feedback system: A feedback system which allows users with any roles to discuss by multiple comments on a transaction.
* Create a Draft Form: Allows the user to temporarily save the form details without having to discard the already written data.
* Categorized Document Upload: Allows different categories for the documents, like prescription, medicine bill, lab test bill, etc.