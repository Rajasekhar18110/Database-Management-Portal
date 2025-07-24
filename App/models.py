from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from .extensions import db
from datetime import datetime, timezone

#UserMixin from flask_login provides default implementations for several methods that Flask-Login requires for user session management and authentication. for ex: is_authenticated, is_active
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    isActive = db.Column(db.String(5), nullable=False, default='no')
    isAdmin = db.Column(db.String(5), nullable=False, default='no')

class UserLogHistory(db.Model):
    __tablename__ = 'UserLogHistory'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, db.ForeignKey('User.email'), nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    last_active = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    logout_time = db.Column(db.DateTime, nullable=True)

class Metric(db.Model):
    __tablename__ = 'Metrics'  # Specify the table name

    MetricName = db.Column(db.String(255), primary_key=True, nullable=False)  
    Description = db.Column(db.Text, nullable=False)  
    DataType = db.Column(db.String(100), nullable=False)  
    EditDate = db.Column(db.DateTime,primary_key=True, default=datetime.now(timezone.utc), nullable=False) 
    DRI = db.Column(db.String(100), nullable=True)
    SignalSource = db.Column(db.String(100), nullable=True)
    LinkedIcMs = db.Column(db.String(100), nullable=True)
    LinkedResearch = db.Column(db.String(100), nullable=True)
    LinkedSpecs = db.Column(db.String(100), nullable=True)
    EditUser = db.Column(db.String(100), nullable=False)


