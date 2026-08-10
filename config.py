import os
from dotenv import load_dotenv

load_dotenv()  # Reads values from .env file

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:1230@localhost/student_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False