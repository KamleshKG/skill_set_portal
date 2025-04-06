from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import  LoginManager
from typing import Optional, cast
from flask_mail import Mail
from app.models.user import User
from prometheus_flask_exporter import PrometheusMetrics
from config import Config
from .extentions import db, login_manager, metrics


# db = SQLAlchemy()
migrate = Migrate()
# login_manager.init_app(app)
mail = Mail()


metrics = PrometheusMetrics.for_app_factory()

# @login_manager.user_loader
# def load_user(user_id):
#     from app.models.user import User  # Import inside function to avoid circular import
#     return User.query.get(int(user_id))
#     return User.query.get(int(user_id))  # Make sure User model has 'id' as primary key

def create_app(config_class=Config):
    app = Flask(__name__)
    # app.config.from_object(config_class)
    app.config.from_object('config.Config')

    
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)
    
    mail.init_app(app)  # Initialize mail with app
    
    login_manager.login_view = 'auth.login'
    metrics.init_app(app)
    
    # Register blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.project_controller import project_bp
    from app.controllers.user_controller import user_bp
    from app.controllers.admin_controller import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(project_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app