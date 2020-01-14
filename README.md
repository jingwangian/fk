# Small flask server system

## Introduce
This is a Flask web server using a Docker container, managed using docker-compose.  The web server will connect to a sqllite db using Flask-SQLAlchemy.  Use flask-migrate to prepare the database. This database will be used to store statistical observations.  
There will be two models. A survey and an observation. 

## Models:
#### Survey:
    Id – primary key
    Name – Varchar/String
#### Observation:
    Id – primary key
    survey_id – foreign key to parent Survey
    value – float
    frequency – count of observations for this value for this entry

## Prerequisite
---
Install the [docker](https://docs.docker.com/v17.09/engine/installation/)

Install the [docker-compose](https://docs.docker.com/compose/install/)


## Start the server:
```
docker-compose up -d
```
When you first run it will build the image, install the required packages, init the database and install some mock data.<br>
Then a link http://{host}:5000/ is used to visit the website where {host} is the host address for your machine. If run in local machine it will be localhost.

### About the mock data
If you want to insert some mock data into the database for easily understanding this system please run the command:
```
make mockdata
```

## Testing:
Run the following command
```
make test
```
Check the testing coverage in the htmlcov/index.html

## Restful APIs:
API | Method| Description
------------- | -------------| -------------
/survey  |POST | Create a new survey
/survey  | GET | List all surveys
/survey/\<id>  |GET | Get a survey
/survey/\<id>  |DELETE | Delete a survey
/stat/\<survery_id>  |POST | Create a new obseration
/stat  | GET | List all observations
/stat/\<id>  |GET | Get a observation by giving observation id
/stat/\<id>  |DELETE | Delete a observation by giving observation id
/stat/\<id>  |PUT | Update a observation by giving observation id

## Install development environment
---
You can install a local development environment. Please follow the following process: 

* Install [Python3.8](https://www.python.org/downloads/)
* Create a directory

    ```
    mkdir flask-server
    cd flask-server
    ```
    
* Create a venv:

    ```
    python3 -m venv venv
    ```

* Install the packages:

    ```
    pip install -r requirements.txt
    ```
    
* Init database and start server:

    ```
    ./scripts/local_start.sh
    ```
