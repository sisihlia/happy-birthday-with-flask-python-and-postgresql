import os

db_name = "mydb"
db_host = "localhost"
db_port = "5432"
db_user = "myuser"
user_password = "mypass"

#db_name = os.environ["DB_NAME"]
#db_host = os.environ["DB_HOST"]
#db_port = os.environ["DB_PORT"]
#db_user = os.environ["DB_USER"]
#user_password = os.environ["USER_PASSWORD"]

SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_DATABASE_URI='postgresql://' + db_user + ':' + user_password + '@' + db_host + '/' + db_name