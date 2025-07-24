from flask import Flask
from flask_login import user_logged_in, user_logged_out, user_accessed, current_user
from .config import DevelopmentConfig
from .extensions import db, login_manager
from .session_manager import check_session_timeout, periodic_check
from .data_access import add_user_login_entry, update_user_logout_entry, update_user_activity_entry
from apscheduler.schedulers.background import BackgroundScheduler

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)   #This will fetch the development config object from config.py and apply those settings to our flask app
    
    db.init_app(app)    #this will bind the flask app (app) to sqlalchemy instance (db)
    login_manager.init_app(app) #Links the LoginManager to the Flask application, allowing it to manage user sessions and handle authentication.
    login_manager.login_view = 'main.login'  # Specifies the route users are redirected to if they try to access a @login_required route without being logged in.
            
    # Initialize APScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=lambda: periodic_check(app), trigger="interval", minutes=5)
    scheduler_flag = True

    if not scheduler.running:
        scheduler.start()

    @app.before_request
    def before_request():
        # if(scheduler_flag):
        #     if not scheduler.running:
        #         scheduler.start()

        if(scheduler.running):
            print('sheduler is running')

        response = check_session_timeout(app)
        if response:  # If session timeout returns a response, return it
            return response
    
    @app.teardown_appcontext
    def shutdown_scheduler(exception=None):
        if(scheduler.running):
            print('scheduler got shutdown')
            scheduler.shutdown()


    #Register blue prints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #If database in the mentioned URI or tables which are defined in models.py do not exist, following code will create them
    with app.app_context():
        db.create_all()

    return app