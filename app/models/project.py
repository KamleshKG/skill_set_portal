from app import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    required_skills = db.relationship('RequiredSkill', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    responses = db.relationship('Response', backref='project', lazy='dynamic')

    def __repr__(self):
        return f'<Project {self.title}>'

class RequiredSkill(db.Model):
    __tablename__ = 'required_skills'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'))
    min_level = db.Column(db.Integer, nullable=False)
    
    skill = db.relationship('Skill')

class Response(db.Model):
    __tablename__ = 'responses'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def accept(self):
        self.status = 'accepted'
        db.session.commit()
    
    def reject(self):
        self.status = 'rejected'
        db.session.commit()