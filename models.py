# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key for user association

class Birthday(db.Model):
    __tablename__ = 'birthdays'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    subject = db.Column(db.String(200), nullable=True)
    message = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(100), nullable=True)  
    
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('birthdays', lazy=True))

class MovieAlert(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    alert_sent = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key for user association
