from app import db
from app.models.incident import Incident
from datetime import datetime

class WorkflowEngine:
    _workflows = {}
    
    @classmethod
    def start_workflow(cls, workflow_type, entity_id):
        workflow_id = f"{workflow_type}_{entity_id}"
        cls._workflows[workflow_id] = {
            'status': 'running',
            'steps': [],
            'current_step': 0,
            'created_at': datetime.utcnow()
        }
        return workflow_id
    
    @classmethod
    def restart_workflow(cls, workflow_type, entity_id):
        workflow_id = f"{workflow_type}_{entity_id}"
        if workflow_id in cls._workflows:
            # Log incident for tracking
            incident = Incident(
                title=f"Workflow restarted: {workflow_type}",
                description=f"Workflow for {entity_id} was restarted",
                workflow_id=workflow_id,
                status='resolved',
                created_at=datetime.utcnow(),
                resolved_at=datetime.utcnow()
            )
            db.session.add(incident)
            db.session.commit()
            
            # Reset workflow
            cls._workflows[workflow_id] = {
                'status': 'running',
                'steps': [],
                'current_step': 0,
                'restarted_at': datetime.utcnow()
            }
            return True
        return False
    
    @classmethod
    def get_workflow_status(cls, workflow_id):
        return cls._workflows.get(workflow_id, {'status': 'not_found'})