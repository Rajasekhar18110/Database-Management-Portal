from flask import  render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from ..data_access import fetch_all_rows, fetch_latest_rows, fetch_row, update_row, fetch_unique_metricnames, fetch_unique_datatypes, fetch_unique_editusers
from ..models import Metric, User
from .. import db

def dashboard_view():
    if(current_user.isActive == 'yes'):
        column_names = Metric.__table__.columns.keys()
        latest_rows = fetch_latest_rows()
        return render_template('dashboard.html',rows = latest_rows, column_names = column_names)
    else:
        flash('You do not have permission to view this page. Please contact the Admin.', 'danger')
        return redirect(url_for('main.login'))

def show_all_view():
    if(current_user.isActive == 'yes'):
        column_names = Metric.__table__.columns.keys()
        allrows = fetch_all_rows()
        MetricNameFilter = fetch_unique_metricnames()
        DataTypeFilter = fetch_unique_datatypes()
        EditUserFilter = fetch_unique_editusers()
        return render_template('all_rows.html',rows = allrows, column_names = column_names, MetricNameFilter = MetricNameFilter, DataTypeFilter = DataTypeFilter, EditUserFilter = EditUserFilter)
    else:
        flash('You do not have permission to view this page. Please contact the Admin.', 'danger')
        return redirect(url_for('main.login'))

def update_view(MetricName):
    if(current_user.isActive == 'yes'):
        if(request.method == 'POST'):
            status = update_row(request)
            if(status == 'success'):
                flash('Successfully updated!', 'success')
                return redirect(url_for('main.dashboard'))
            
            if(status == 'failure'):
                flash('An error occurred while updating. Please try again.', 'danger')

        row = fetch_row(MetricName)
        return render_template('update.html', row = row)
    
    else:
        flash('You do not have permission to view this page. Please contact the Admin.', 'danger')
        return redirect(url_for('main.login'))
