# 📊 Database Management Website

A secure, fullstack web application built with **Flask** to manage and maintain a centralized **Metrics Database**. Designed for teams responsible for tracking and updating metric definitions, with role-based access and admin privileges.

---

## 🔧 Features

- **User Authentication**: Secure login system using `Flask-Login`. Passwords are encrypted before being stored in the database.
- **Session Management**: Automatic logout for inactive users to enhance security.
- **Role-Based Access**:
  - **Admin**: Can view additional pages like the admin dashboard and log history.
  - **Regular Users**: Can view and update metric definitions.
- **Admin Dashboard**:
  - Activate or deactivate users.
  - Only active users can access the main dashboard.
- **Main Dashboard**:
  - View metric definitions and last edited information.
  - Update definitions directly from the UI, with changes reflected in the database.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask  
- **Authentication**: Flask-Login  
- **Database**: SQLite (via SQLAlchemy)  
- **Frontend**: HTML,CSS

---

## 👤 User Roles

| Role   | Access Level |
|--------|--------------|
| Admin  | Full access to all pages and user management |
| User   | Access to dashboard and metric updates |

---

## ⚙️ Project Setup

This project uses a modular Flask application structure with blueprints, configuration management, and background scheduling.

### 🔑 App Initialization (`__init__.py`)

- Loads configuration from `DevelopmentConfig`
- Initializes SQLAlchemy and Flask-Login
- Registers blueprints and sets up user loader
- Starts a background scheduler to monitor session timeouts
- Creates database tables if they don’t exist

---

## 🗃️ Database Access Layer (`data_access.py`)

Handles all SQL operations and interactions with the database.

### Metrics Table Operations

- `fetch_all_rows()`, `fetch_latest_rows()`, `fetch_row()`
- `update_row(request)`: Inserts updated metric entries

### Filters

- `fetch_unique_metricnames()`, `fetch_unique_datatypes()`, `fetch_unique_editusers()`

### User Management

- `fetch_all_users()`, `fetch_user(email)`, `update_user_permission(request)`

### User Activity Logging

- `add_user_login_entry(user)`, `update_user_logout_entry(user)`, `update_user_activity_entry(user)`
- `fetch_user_log_history()`

---

## ⏱️ Session Management (`session_manager.py`)

Ensures secure session handling and automatic logout for inactive users.

### `check_session_timeout(app)`

- Validates session activity
- Logs out users if session expires
- Updates last activity timestamp

### `periodic_check(app)`

- Runs every 5 minutes via APScheduler
- Updates logout time for users who closed the browser or lost session unexpectedly

---

## 🌐 Routing Overview (`routing.py`)

Defines all URL routes using Flask Blueprints.

| Route | Method(s) | Access | Description |
|-------|-----------|--------|-------------|
| `/` | GET, POST | Public | Login page |
| `/register` | GET, POST | Public | User registration |
| `/logout` | POST | Authenticated | Logs out the current user |
| `/dashboard` | GET | Authenticated | Main dashboard for users |
| `/showAll` | GET | Authenticated | Displays all metric entries |
| `/profile` | GET | Authenticated | User profile page |
| `/admin_dashboard` | GET | Admin only | Admin dashboard |
| `/update/<MetricName>` | GET, POST | Authenticated | Update a specific metric |
| `/update_user
