# happy-birthday-with-flask-python-and-postgresql

# Activate venv
$ python -m venv env

# Source venv
$ source env/bin/activate

# Create DB
$ python
>> from app import db
>> db.create_all()
>> exit()

# Run Server (http://localhst:5000)
python app.py
