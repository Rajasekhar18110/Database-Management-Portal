#this module takes care of session timeout. if the user is inactive for sometime. he will automatically get logged out

from datetime import datetime, timezone
from flask import session, redirect, url_for, flash, current_app
from flask_login import logout_user, current_user
from .data_access import update_user_activity_entry, update_user_logout_entry
from . import db
from sqlalchemy.sql import text

def check_session_timeout(app):
    
    #case1: session object is not empty. that means user is authenticated and session object have last_active field.
    if 'last_activity' in session:      #session has not expired
        now = datetime.now(tz=timezone.utc) 
        last_activity = session['last_activity']
        timeout = app.config['PERMANENT_SESSION_LIFETIME']

        if now - datetime.fromisoformat(last_activity) <= timeout: #session has not expired, so update the last_active time in the database
            if(current_user.is_authenticated):
                update_user_activity_entry(current_user)
    
    #case2: session has expired. so session object will be empty. but we can access user details from remember_me functionality of flask_login.
    if(('last_activity' not in session) and (current_user.is_authenticated)):
        update_user_logout_entry(current_user)
        session.clear()
        logout_user()
        
        flash('Your session has expired. Please login again.','session_expired')
        return redirect(url_for('main.login'))

    
    #before every request, update last_activity in session. 
    session['last_activity'] = datetime.now(tz=timezone.utc).isoformat()


#incase user opened the website in incognito and closed the tab without logging out or flask session abruptly ends, then logout time might not update in the database. so the below function periodically checks in the database if any user's session has expired and logout entry has not updated and it will update it
def periodic_check(app):
    print('periodic check function is called')
    with app.app_context():
        current_time = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        
        query = text("""
                UPDATE UserLogHistory
                SET logout_time = :logout_time
                WHERE logout_time IS NULL AND 
                      ((julianday(:current_time) - julianday(last_active)) * 86400) > :timeout;
                """)
        
        db.session.execute(query, {
        'logout_time': current_time,
        'current_time': current_time,
        'timeout': app.config['PERMANENT_SESSION_LIFETIME'].total_seconds()
        })
        
        db.session.commit()