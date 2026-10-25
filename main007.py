from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from datetime import datetime, date

app=Flask(__name__)

"""
@app.route('/', methods=['GET'])
def home():
  return jsonify(
    {
        'name':'she',
        'msg':'welcome'
    })
"""
basedir=os.path.abspath(os.path.dirname(__file__))
print(basedir)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db=SQLAlchemy(app)
ma=Marshmallow(app)

class User(db.Model):
  __tablename__='employee'
  id=db.Column(db.Integer,primary_key=True)
  name=db.Column(db.String(100))
  contact=db.Column(db.String(100), unique=True)
  email=db.Column(db.String(50), unique=True)
  doh=db.Column(db.String(50))
  #doh=db.Column(db.DateTime())
  #salry=db.Column(db.float)

  def __init__(self, name, contact, email, doh):
    self.name=name
    self.contact=contact
    self.email=email
    self.doh=doh
   # self.salry=salry

class UserSchema(ma.Schema):
  class Meta:
    fields=('id','name','contact','email','doh')

user_schema= UserSchema()
users_schema=UserSchema(many=True)

#Add new user
@app.route('/user',methods=['POST'])
def add_user():
  name=request.json['name']
  contact=request.json['contact']
  email=request.json['email']
  doh=request.json['doh']
 # salry=request.json['salry']
  new_user = User(name, contact, email, doh)
  db.session.add(new_user)
  db.session.commit()
  return user_schema.jsonify(new_user)

#show all
@app.route('/user',methods=['GET'])
def getAllUser():
  all_users=User.query.all()
  result=users_schema.dump(all_users)
  return jsonify(result)


@app.route('/user/<id>', methods=['GET'])
def getUserByid(id):
  user=User.query.get(id)
  return user_schema.jsonify(user)

@app.route('/user/<id>', methods=['PUT'])
def UpdateUser(id):
  user=User.query.get(id)
  name=request.json['name']
  contact=request.json['contact']
  email=request.json['email']
  doh=request.json['doh']
  #salry=request.json['salry']
  user.name=name
  user.contact=contact
  user.email=email
  user.doh=doh
  #user.salry=salry
  db.session.commit()
  return user_schema.jsonify(user)

@app.route('/user/<id>',methods=['DELETE'])
def DeleteUserById(id):
  user=User.query.get(id)
  db.session.delete(user)
  db.session.commit()
  return user_schema.jsonify(user)

with app.app_context():
    db.create_all()

if __name__=='__main__':
  app.run(debug=True, port=5000)