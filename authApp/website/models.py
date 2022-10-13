from random import choices
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func




class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000))
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.String(50))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.String(50))
    password = db.Column(db.String(150))
    # first_name = db.Column(db.String(150))
    employees = db.relationship('Employee')




class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    state = db.Column(db.String(250))

