# REST API with Flask and SQL Alchemy


A Flask based RESTful API using SQLAlchemy to communicate with PostgreSQL

## Quick Start Using Venv
    # Activate venv
    $ python -m venv env
    $ source env/bin/activate
    
    #Install dependencies
    $ pip install -r requirements.txt

    # Create DB
    $ python
    >> from app import db
    >> db.create_all()
    >> exit()

    # Run Server (http://localhost:5000)
    $ python app.py
          
    #Test Server (http://localhost:5000)
    $ python -m unittest -v

## API

| HTTP  | Endpoint             | Description                                       |
| ------|----------------------| --------------------------------------------------|
| GET   | /hello               | get all birthdates                                |
| GET   | /hello/name          | get a birthdate by name                           |
| PUT   | /hello/name data {}  | create(if name not exist)/update a name-birthdate |
| POST  | /hello data {}       | create a name-birthdate                           |
