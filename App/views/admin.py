from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from ..data_access import fetch_all_users, fetch_user, update_user_permission, fetch_user_log_history
from ..models import Metric, User
from .. import db

def admin_dashboard_view():
    if(current_user.isAdmin == 'yes'):
        column_names = ['Username','email','isActive','isAdmin']
        users = fetch_all_users()
        return render_template('admin_dashboard.html',users = users, column_names = column_names)
    else:
        flash('You do not have permission to view this page. Please contact the Admin.', 'danger')
        return redirect(url_for('main.login'))
    
def update_user_view(email):
    if(current_user.isAdmin == 'yes'):
        if(request.method == 'POST'):
            status = update_user_permission(request)
            if(status == 'success'):
                flash('Successfully updated!', 'success')
                return redirect(url_for('main.admin_dashboard'))
            
            if(status == 'failure'):
                flash('An error occurred while updating. Please try again.', 'danger')

        row = fetch_user(email)
        return render_template('update_user.html', row = row)
    
    else:
        flash('You do not have permission to view this page. Please contact the Admin.', 'danger')
        return redirect(url_for('main.login'))
    
def log_history_view():
    if(current_user.isAdmin == 'yes'):
        column_names = ['id','username','email','login time','last active','logout time']
        user_log_history = fetch_user_log_history()
        return render_template('log_history.html', column_names=column_names, user_log_history=user_log_history)
    else:
        flash('You do not have permission to view this page. Please contact the Admin.', 'danger')
        return redirect(url_for('main.login'))


    