import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()   #this will load the environment variables in .env file (file containing sensitive information like URLs, username and passwords, OpenAI keys etc)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)  #This will disables a feature that tracks object modifications in SQLAlchemy, which is unnecessary and can cause overhead. setting it to False will avoid warnings in logs.
    PERMANENT_SESSION_LIFETIME= timedelta(minutes=int(os.getenv('PERMANENT_SESSION_LIFETIME', 2)))
    DEBUG = False   #by default its in production environment

class DevelopmentConfig(Config):
    DEBUG = True    #in development environment we set DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
