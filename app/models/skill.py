from app import db

class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    # Relationships
    users = db.relationship('UserSkill', back_populates='skill')
    required_in = db.relationship('RequiredSkill', back_populates='skill')

class UserSkill(db.Model):
    __tablename__ = 'user_skills'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'))
    level = db.Column(db.Integer, nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='skills')
    skill = db.relationship('Skill', back_populates='users')