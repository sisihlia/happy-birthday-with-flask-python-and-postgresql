import os

db_name = "mydb"
db_host = "localhost"
db_port = "5432"
db_user = "myuser"
user_password = "mypass"

SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_DATABASE_URI='postgresql://' + db_user + ':' + user_password + '@' + db_host + '/' + db_name