from app import db
from datetime import datetime

class Incident(db.Model):
    __tablename__ = 'incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    workflow_id = db.Column(db.String(50))
    status = db.Column(db.String(20), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def resolve(self, user_id):
        self.status = 'resolved'
        self.resolved_at = datetime.utcnow()
        self.resolved_by = user_id
        db.session.commit()