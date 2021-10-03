from itertools import count
from flask import Flask,jsonify, request,json
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from datetime import date,datetime
import re


app = Flask(__name__)

app.config.from_pyfile('conf/psql-config.py')

db=SQLAlchemy(app)
class Birthdates(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(255), nullable=False)
    birth_date=db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_name(cls,name):
        return cls.query.filter_by(name=name).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class BirthdatesSchema(Schema):
    id=fields.Integer()
    name=fields.String()
    birth_date=fields.String()


def serialize_birthdate(data,many):
    if many:
        serializer=BirthdatesSchema(many=True)
    else:
        serializer=BirthdatesSchema()
    return serializer.dump(data)

def create_birthdate_cmd():
    data=request.get_json()
    name = data.get('name')
    if not name.isalpha():
        return name_is_invalid(name)
    if (parse_birthdate() < date.today()):
        return birthdate_is_invalid()
    new_birthdate=Birthdates(
        name=name,
        birth_date=data.get('birth_date')
    )
    new_birthdate.save()
    return jsonify(serialize_birthdate(new_birthdate,False)),204

def update_birthdate_cmd(id):
    birthdate_to_update=Birthdates.get_by_id(id)
    data=request.get_json()
    birthdate_to_update.name=data.get('name')
    birthdate_to_update.birth_date=data.get('birth_date')
    db.session.commit()
    return jsonify(serialize_birthdate(birthdate_to_update,False)),204


@app.route('/hello/<int:id>', methods=['PUT'])
def update_birthdate(id):
    return update_birthdate_cmd(id)

@app.route('/hello/<int:id>', methods=['DELETE'])
def delete_birthdate_by_id(id):
    birthdate_to_delete=Birthdates.get_by_id(id)
    birthdate_to_delete.delete()
    return jsonify({"message":"Deleted"}),200

@app.route('/hello/<string:name>', methods=['DELETE'])
def delete_birthdate_by_name(name):
    birthdate=Birthdates.get_by_name(name)
    if (len(birthdate) != 1):
        return resource_not_valid_by_name(birthdate)
    else:
        birthdate[0].delete()
        return jsonify({"message":"Deleted"}),200

@app.route('/hello', methods=['GET'])
def get_all_birthdates():
    birthdates=Birthdates.get_all()
    return jsonify(serialize_birthdate(birthdates,True)),200

@app.route('/hello', methods=['POST'])
def create_birthdate():
    return create_birthdate_cmd()

def name_is_invalid(name):
    return jsonify({"message": name +" is invalid argument, Name must contain only letters"}),400

def birthdate_is_invalid():
    return jsonify({"message": "Birth_date is invalid argument, Birth_date must be before today"}),400

def parse_birthdate():
    mydate=request.get_json().get('birth_date')
    today = date.today()
    return datetime.strptime(mydate, '%Y-%m-%d').date().replace(year=today.year)

@app.route('/hello/<string:name>', methods=['PUT'])
def create__or_update_birthdate_by_name(name):
    special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if(special_char.search(name) == None):
        print('String does not contain any special characters.')
    else:
        print('The string contains special characters.')
    if (not name.isalpha() or special_char.search(name) != None) :
        return name_is_invalid(name)
    if (parse_birthdate() < date.today()):
        return birthdate_is_invalid()
    birthdate_to_update=Birthdates.get_by_name(name)
    if not birthdate_to_update:
        new_birthdate=Birthdates(
        name=name,
        birth_date=request.get_json().get('birth_date')
            )
        new_birthdate.save()
        return jsonify(serialize_birthdate(new_birthdate,False)),204
    else:
        data=request.get_json()
        birthdate_to_update[0].birth_date=data.get('birth_date')
        db.session.commit()
        return jsonify(serialize_birthdate(birthdate_to_update,False)),204

@app.route('/hello/<int:id>', methods=['GET'])
def get_birthdate(id):
    birthdate=Birthdates.get_by_id(id)
    return  hello_birthday(count_birthday(birthdate.birth_date, date.today()),birthdate.name)

def resource_not_valid_by_name(birthdate):
    if len(birthdate) == 0 :
        return jsonify({"message":"Resource not found"}),404
    if len(birthdate) > 1:
        return jsonify({"message":"More than one resources with the same name found. Query the birthday with the id.. "}),400   


@app.route('/hello/<string:name>', methods=['GET'])
def get_birthdate_by_name(name):
    birthdate=Birthdates.get_by_name(name)
    if (len(birthdate) != 1):
        return resource_not_valid_by_name(birthdate)
    else:
        return  hello_birthday(count_birthday(birthdate[0].birth_date, date.today()),name)

def count_birthday(birthdate,today):
    date_time_obj = datetime.strptime(birthdate, '%Y-%m-%d')
    date_obj=date_time_obj.date()
    birth = date_obj
    today = date.today()
    if(
        today.month == birth.month
        and today.day >= birth.day
        or today.month > birth.month
    ):
        nextBirthdayYear = today.year + 1
    else:
        nextBirthdayYear = today.year
    nextBirthday = date(
        nextBirthdayYear, birth.month, birth.day
    )
    return (nextBirthday - today).days


def hello_birthday(diff,name):
    if diff==365:
        return jsonify({"message":"Hello, "+ name +"! Happy birthday" }),200
    else:
        return jsonify({"message":"Hello, "+ name +"! Your birthday is in " + str(diff)+ " days" }),200

@app.errorhandler(500)
def internal_server(error):
    return jsonify({"message":"Server Error"}),500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"message":"Resource not found"}),404

# Run Server
if __name__ == '__main__':
  app.run(debug=True)