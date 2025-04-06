from app import db
from app.models.incident import Incident
from datetime import datetime

class WorkflowService:
    _workflows = {}
    
    @classmethod
    def start_workflow(cls, workflow_type, entity_id, initiator_id):
        workflow_id = f"{workflow_type}_{entity_id}"
        cls._workflows[workflow_id] = {
            'status': 'running',
            'current_step': 0,
            'created_at': datetime.utcnow(),
            'history': []
        }
        return workflow_id
    
    @classmethod
    def restart_workflow(cls, workflow_id, user_id):
        if workflow_id in cls._workflows:
            # Log incident
            incident = Incident(
                title=f"Workflow {workflow_id} restarted",
                description=f"Manual restart by user {user_id}",
                workflow_id=workflow_id,
                status='resolved',
                resolved_by=user_id
            )
            db.session.add(incident)
            db.session.commit()
            
            # Reset workflow
            cls._workflows[workflow_id] = {
                'status': 'running',
                'current_step': 0,
                'restarted_at': datetime.utcnow(),
                'history': []
            }
            return True
        return False