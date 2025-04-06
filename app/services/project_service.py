from app import db
from app.models.project import Project, RequiredSkill, Response
from app.models.user import User
from app.services.notification_service import NotificationService
from app.utils.workflow_engine import WorkflowEngine
from datetime import datetime


class ProjectService:
    @staticmethod
    def create_project(title, description, required_skills, creator_id):
        project = Project(
            title=title,
            description=description,
            created_by=creator_id,
            created_at=datetime.utcnow(),
            status='open'
        )
        
        db.session.add(project)
        db.session.commit()
        
        for skill_id, min_level in required_skills.items():
            req_skill = RequiredSkill(
                project_id=project.id,
                skill_id=skill_id,
                min_level=min_level
            )
            db.session.add(req_skill)
        
        db.session.commit()
        
        # Start workflow
        WorkflowEngine.start_workflow('project_creation', project.id)
        
        # Notify users
        NotificationService.notify_new_project(project)
        
        return project
    
    @staticmethod
    def get_projects_for_user(user_id):
        user = User.query.get(user_id)
        user_skill_ids = [us.skill_id for us in user.skills.all()]
        
        projects = Project.query.join(RequiredSkill)\
            .filter(RequiredSkill.skill_id.in_(user_skill_ids))\
            .filter(Project.status == 'open')\
            .all()
            
        return projects
    
    @staticmethod
    def create_response(project_id, user_id, message):
        response = Response(
            project_id=project_id,
            user_id=user_id,
            message=message,
            status='pending',
            created_at=datetime.utcnow()
        )
        
        db.session.add(response)
        db.session.commit()
        
        # Notify admin
        NotificationService.notify_new_response(response)
        
        return response
    
    @staticmethod
    def restart_project_workflow(project_id):
        project = Project.query.get(project_id)
        if project:
            WorkflowEngine.restart_workflow('project_creation', project.id)
            return True
        return False