from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from .views.auth import login_view, register_view, logout_view
from .views.dashboard import dashboard_view, show_all_view, update_view
from .views.admin import admin_dashboard_view, update_user_view, log_history_view
from . import db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def login():
    return login_view()


@main.route('/register', methods=['GET', 'POST'])
def register():
    return register_view()
    

@main.route('/logout', methods=['POST'])
@login_required
def logout():
    return logout_view()

@main.route('/dashboard')
@login_required
def dashboard():
    return dashboard_view()


@main.route('/showAll')
@login_required
def Show_allrows():
    return show_all_view()

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main.route('/admin_dashboard')
@login_required
def admin_dashboard():
    return admin_dashboard_view()

@main.route('/update/<MetricName>', methods=['GET','POST'])
@login_required
def update(MetricName):
    return update_view(MetricName)

@main.route('/update_user/<email>', methods=['GET','POST'])
@login_required
def update_user(email):
    return update_user_view(email)

@main.route('/log_history')
@login_required
def log_history():
    return log_history_view()
    