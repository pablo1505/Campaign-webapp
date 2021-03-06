# Backend
This repo is just the backend portion of this project.  

## Prerequisites
### You might need to have the following softwares:
* Python 3.6
* PostgreSQL

### You might need to install the following packages:
* virtualenv
* flask
* psycopg2
* requests

## Getting Started
Download necessary softwares and packages first.  
If you activate virtualenv called "venv" you won't need the libraries below. Instructions are below so keep reading.

### Remote host and database
All backend APIs does not currently have a remote host.
The following callable links can be found at:
```
./api_list.txt
```

### Local host and database
If you want to set up in local database follow the steps below.
  
#### Modify Database
Setup your PostgreSQL database.  
You must first edit the code so that it matches your SQL credentials in this file:
```
cd ./base_cmd/db_commands
```
Then you should modify line 29 to match your own variables
  
#### Modify Flask Call
To run in a local host, you must make sure that the file at:
```
$ ./call_flask.sh
```
  
#### Getting the Data
In order to match python version and libraries you must run the following bash command:
```
$ source ./venv/bin/activate
``` 
Or if you are in cmd-prompt, you can run:
```
"venv/Scripts/activate.bat"
```

Finally we can create the database with the following command:
```
py ./base_cmd/create_db.py
```
  
#### Running the localhost
Then run the localhost using the bash command:
```
$ ./call_flask.sh
```
Then on your command prompt, we can first create a user.
Here is an example:
```
curl http://localhost:3000/user/create-user -d "{\"usertype\": \"influencer\", "\"comp_name\": \"banana\", "\"name\": \"banana\", \"borough\":\"Manhattan\", \"state\": \"NY\",  "\"phone\":\"718-239-4738\", \"email\":\"banana@b.\", \"password\":\"bananahana\"}" -H "Content-Type: application/json"
```
Then we can login to that user using the following command
```
curl http://localhost:3000/user/login -d "{\"email\": \"banana@b.\", \"password\": \"bananahana\"}" -H "Content-Type: application/json"
```