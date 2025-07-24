#this file contains functions/SQL queries to interact with the database
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from . import db
from sqlalchemy.sql import text
from flask_login import current_user, user_logged_in, user_logged_out, user_accessed
from flask import flash, redirect, url_for, session
from datetime import datetime, timezone
from .models import UserLogHistory


def fetch_all_rows():
    """Fetch all rows from the 'Metrics' table."""
    query = text('SELECT * FROM Metrics ORDER BY MetricName,EditDate DESC')
    result = db.session.execute(query)
    return result.fetchall()

def fetch_latest_rows():
    """Fetch latest edited rows from the Metrics table"""
    query = text(
            """
            WITH CTE AS (   
            SELECT *,          
            ROW_NUMBER() OVER (PARTITION BY MetricName ORDER BY EditDate DESC) AS rn   
            FROM Metrics)
            SELECT MetricName, Description, DataType, EditDate, DRI, SignalSource, LinkedIcMs, LinkedResearch, LinkedSpecs, EditUser
            FROM CTE WHERE rn = 1
            """
            )
    
    result = db.session.execute(query)
    return result.fetchall()

def fetch_row(MetricName):
    query = text("SELECT * FROM Metrics WHERE MetricName= :metricname ORDER BY EditDate DESC")
    result = db.session.execute(query, {"metricname": MetricName})

    return result.fetchone()

def update_row(request):
    new_metric_name = request.form['metric-name']
    new_description = request.form['description']
    new_datatype = request.form['data-type']

    if(request.form['dri'] == 'None'):
        new_DRI = None
    else:
        new_DRI = request.form['dri']
    
    if(request.form['signal-source'] == 'None'):
        new_signal_source = None
    else:
        new_signal_source = request.form['signal-source']

    if(request.form['linked-icms'] == 'None'):
        new_linkedIcMs = None
    else:
        new_linkedIcMs = request.form['linked-icms']

    if(request.form['linked-research'] == 'None'):
        new_linkedResearch = None
    else:
        new_linkedResearch = request.form['linked-research']

    if(request.form['linked-specs'] == 'None'):
        new_linkedSpecs = None
    else:
        new_linkedSpecs = request.form['linked-specs']

    new_edit_user = current_user.username

    try:
        query = text("INSERT INTO Metrics VALUES (:metricname, :description, :datatype, DATETIME('now'), :dri, :signal_source, :linked_icms, :linked_research, :linked_specs, :edituser)")

        db.session.execute(query, {"metricname": new_metric_name, "description":new_description, "datatype": new_datatype, "dri": new_DRI, "signal_source": new_signal_source, "linked_icms":new_linkedIcMs, "linked_research": new_linkedResearch, "linked_specs": new_linkedSpecs, "edituser": new_edit_user })

        db.session.commit()
        return 'success'
    
    except Exception as e:
        db.session.rollback()  # Rollback if there's an error
        print(str(e))  # For debugging purposes

        return 'failure'
    
def fetch_unique_metricnames():
    query = text("SELECT DISTINCT MetricName FROM Metrics")
    result = db.session.execute(query)

    return result.fetchall()

def fetch_unique_datatypes():
    query = text("SELECT DISTINCT DataType FROM Metrics")
    result = db.session.execute(query)

    return result.fetchall()

def fetch_unique_editusers():
    query = text("SELECT DISTINCT EditUser FROM Metrics")
    result = db.session.execute(query)

    return result.fetchall()
            

def fetch_all_users():
    """Fetch all rows from the 'user' table."""
    query = text('SELECT username,email,isActive,isAdmin FROM user')
    result = db.session.execute(query)
    return result.fetchall()

def fetch_user(email):
    query = text("SELECT username,email,isActive,isAdmin FROM user WHERE email= :email")
    result = db.session.execute(query, {"email": email})

    return result.fetchone()

def update_user_permission(request):
    isActive = request.form['isActive']
    isAdmin = request.form['isAdmin']
    email = request.form['email']

    try:
        query = text("UPDATE user SET isActive=:isActive , isAdmin=:isAdmin where email=:email")

        db.session.execute(query, {"isActive": isActive, "isAdmin":isAdmin, "email": email})
        db.session.commit()
        return 'success'
    
    except Exception as e:
        db.session.rollback()  # Rollback if there's an error
        print(str(e))  # For debugging purposes

        return 'failure'


def add_user_login_entry(user):
    current_time = datetime.now(tz=timezone.utc)
    
    query = text("""
            INSERT INTO UserLogHistory (username, email, login_time, last_active, logout_time)
            VALUES ( :username, :email, :login_time, :last_active, NULL);
            """)

    db.session.execute(query, {
    'username': user.username,
    'email': user.email,
    'login_time': current_time.strftime("%Y-%m-%d %H:%M:%S"),
    'last_active': current_time.strftime("%Y-%m-%d %H:%M:%S")
    })
    
    db.session.commit()

def update_user_logout_entry(user):
    
    current_time = datetime.now(tz=timezone.utc)
    
    query = text("""
            UPDATE UserLogHistory
            SET logout_time = :logout_time
            WHERE id = (
                SELECT id
                FROM UserLogHistory
                WHERE email = :email AND logout_time IS NULL
                ORDER BY id DESC
                LIMIT 1
            );
            """)
    
    db.session.execute(query, {
    'logout_time': current_time.strftime("%Y-%m-%d %H:%M:%S"),
    'email': user.email,
    })
    
    db.session.commit()

def update_user_activity_entry(user):
    current_time = datetime.now(tz=timezone.utc)
    
    query = text("""
            UPDATE UserLogHistory
            SET last_active = :last_active
            WHERE id = (
                SELECT id
                FROM UserLogHistory
                WHERE email = :email AND logout_time IS NULL
                ORDER BY id DESC
                LIMIT 1
            );
            """)
    
    db.session.execute(query, {
    'last_active': current_time.strftime("%Y-%m-%d %H:%M:%S"),
    'email': user.email,
    })
    
    db.session.commit()

def fetch_user_log_history():
    """Fetch all rows from the 'UserLogHistory' table."""
    query = text('SELECT * FROM UserLogHistory ORDER BY login_time DESC')
    result = db.session.execute(query)
    return result.fetchall()