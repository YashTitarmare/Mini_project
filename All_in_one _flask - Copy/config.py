# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:python@localhost:5432/planner_db'

    SECRET_KEY = os.urandom(24)
