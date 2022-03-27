## To dumpdata in db.json 
> python3 manage.py dumpdata > dummyData/db.json
### Dumping specific models 
> python3 manage.py dumpdata user.User user.Patient user.Doctor user.HCAdmin user.Accounts> dummyData/login.json
## To load data into database
> python3 manage.py loaddata dummyData/db.json  

### Login.json
* password = corresponding username 