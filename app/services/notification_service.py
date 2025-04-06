from flask import current_app
from flask_mail import Message
from threading import Thread

class NotificationService:
    @staticmethod
    def send_email(subject, recipients, text_body, html_body=None):
        """Send an email asynchronously"""
        msg = Message(
            subject,
            recipients=recipients,
            body=text_body,
            html=html_body
        )
        Thread(
            target=NotificationService._send_async_email,
            args=(current_app._get_current_object(), msg)
        ).start()

    @staticmethod
    def _send_async_email(app, msg):
        """Background email sending task"""
        with app.app_context():
            app.extensions['mail'].send(msg)

    @staticmethod
    def notify_new_project(project):
        """Notify relevant users about a new project"""
        from app.models.user import User  # Avoid circular imports
        
        # Example: Notify admin
        admin = User.query.filter_by(is_admin=True).first()
        if admin:
            NotificationService.send_email(
                subject=f"New Project: {project.title}",
                recipients=[admin.email],
                text_body=f"A new project '{project.title}' has been created."
            )

    @staticmethod
    def notify_new_response(response):
        """Notify project creator about a new response"""
        NotificationService.send_email(
            subject=f"New Response for Project: {response.project.title}",
            recipients=[response.project.creator.email],
            text_body=f"You have a new response from {response.responder.name}"
        )