from flask import render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from ..models import User
from .. import db
from ..data_access import add_user_login_entry, update_user_logout_entry
from datetime import timedelta

def login_view():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate email
        if not email.endswith("@microsoft.com"):
            flash("Email must end with @microsoft.com", "danger")
            return redirect(url_for('main.login'))
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True, duration=timedelta(hours=3))
            add_user_login_entry(current_user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid credentials.', 'danger')

    return render_template('login.html')


def register_view():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate email
        if not email.endswith("@microsoft.com"):
            flash("Email must end with @microsoft.com", "danger")
            return redirect(url_for('main.register'))

        # Validate password length
        if len(password) < 8:
            flash("Password must be at least 8 characters long", "danger")
            return redirect(url_for('main.register'))
        
        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("User with this email already exists", "danger")
            return redirect(url_for('main.register'))
        
        hashed_password = generate_password_hash(password)

        new_user = User(username=username, email=email, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()  # Rollback if there's an error
            flash('An error occurred while registering. Please try again.', 'danger')
            print(str(e))  # For debugging purposes

    return render_template('register.html')

def logout_view():
    update_user_logout_entry(current_user)
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('main.login'))
