from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
#UserMixin is a module that:
# authenticates user credentials
# checks if the user's account is active
# checks if the user is an anonymous user
# has a get_id that can return the unique id for a user object

class Task(db.Model):
    #creates a table that stores user tasks unique to them using their ID
    #this uses a one to many relationship (one user with many tasks)
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    title = db.Column(db.String(10000)) #stores task title
    duration = db.Column(db.String(10000)) #task duration stored
    completion_date = db.Column(db.DateTime, nullable=True) #time/date stored
    priority = db.Column(db.String(10), nullable=False) #task priority stored
    #used to connect this table with the table used to store user information
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', back_populates='tasks')

class User(db.Model, UserMixin):
    #Creates a table to store user related info
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    tasks = db.relationship('Task', back_populates='user', cascade='all, delete-orphan')