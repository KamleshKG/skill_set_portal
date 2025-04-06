from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from prometheus_flask_exporter import PrometheusMetrics
from typing import Any
# from .prometheus_stubs import PrometheusMetrics


db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
# metrics = PrometheusMetrics()  # type: ignore

# Initialize extensions without app context
# db = SQLAlchemy()
# login_manager = LoginManager()
# mail = Mail()
# # metrics = PrometheusMetrics() 

metrics = None

def init_metrics(app):
    global metrics
    metrics = PrometheusMetrics(app)  # Now initialized with app
    return metrics

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login user loader callback"""
    from app.models.user import User  # Local import avoids circular imports
    return User.query.get(int(user_id))