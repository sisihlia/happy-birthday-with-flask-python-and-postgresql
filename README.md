# REST API with Flask and SQL Alchemy

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
