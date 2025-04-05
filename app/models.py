# ------------------  Database Models ------------------
from unicodedata import name
from .import db
#from .models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                       String, ForeignKey
                       
"""
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    email = db.Column(db.String(256), index=True, unique=True)  # index => should not be duplicate
    posts = db.relationship('Post', backref='author')

    def __repr__(self):
        return '<User %r>' % self.email


class Post(db.Model):
    __tablename__ = 'posts'
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(256))
    body        = db.Column(db.Text)
    author_id   = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>' % self.title"""


# Define models
roles_users = db.Table('roles_users',
                        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model) :      #, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repre__(self):
        return '<Role %r>' % self.name
        
class User(db.Model) :              # UserMixin, db.Model):
    __tablename__ = 'user'
    id                  = db.Column(db.Integer, primary_key=True)
    email 		        = db.Column(db.String(100), unique=True)
    password 		    = db.Column(db.String(255))
    #username 		    = db.Column(db.String(100), unique=True)
    last_login_at 	    = db.Column(db.DateTime())
    current_login_at 	= db.Column(db.DateTime())
    last_login_ip 	    = db.Column(db.String(100))
    current_login_ip 	= db.Column(db.String(100))
    login_count 	    = db.Column(db.Integer)
    active 		        = db.Column(db.Boolean()) 
    confirmed_at 	    = db.Column(db.DateTime())
    firstname 		    = db.Column(db.String(255))
    lastname 		    = db.Column(db.String(255)) 
    phonenumber 	    = db.Column(db.String(100), unique=True)
    altnumber		    = db.Column(db.String(100))
    designation	        = db.Column(db.String(100))
    location		    = db.Column(db.String(100))
    city		        = db.Column(db.String(100))
    state 		        = db.Column(db.String(100))
    country 		    = db.Column(db.String(100))
    zip_code		    = db.Column(db.String(100))
    roles 		        = db.relationship('Role', secondary=roles_users, 
                            backref=db.backref('users', lazy='dynamic')) 
    def __repr__(self):
        return '<User %r>' % self.email

class Nonce(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nonce = db.Column(db.String(64), unique=True, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)  # UNIX timestamp

    def __repr__(self):
        return f"<Nonce {self.nonce[:8]}... at {self.timestamp}>"

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)  # UNIX timestamp
    payload = db.Column(db.Text, nullable=False)  # Stores JSON data

    def __repr__(self):
        return f"<Attendance Student: {self.student_id}, Time: {self.timestamp}>"

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instructor_id = db.Column(db.String(50), nullable=False)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_level = db.Column(db.String(10), nullable=False)
    course_code = db.Column(db.String(500), nullable=False)
    lecture_start = db.Column(db.DateTime, nullable=False)
    lecture_end = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Course {self.course_code} - {self.instructor_id}>"
