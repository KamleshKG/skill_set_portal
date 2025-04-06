from flask import Blueprint, render_template, flash, redirect, url_for,request
from flask_login import login_required, current_user
from app.models.user import User
from app.models.skill import Skill, UserSkill
from app import db
from app.models.user import User
from app.models.skill import Skill, UserSkill 

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile')
@login_required
def profile():
    user_skills = UserSkill.query.filter_by(user_id=current_user.id).all()
    all_skills = Skill.query.all()
    return render_template('user/profile.html', 
                         user=current_user,
                         user_skills=user_skills,
                         all_skills=all_skills)

@user_bp.route('/add-skill', methods=['POST'])
@login_required
def add_skill():
    skill_id = request.form.get('skill_id')
    level = request.form.get('level', type=int)
    
    if not skill_id or not level:
        flash('Please select a skill and level')
        return redirect(url_for('user.profile'))
    
    # Check if user already has this skill
    existing = UserSkill.query.filter_by(
        user_id=current_user.id,
        skill_id=skill_id
    ).first()
    
    if existing:
        existing.level = level
    else:
        new_skill = UserSkill(
            user_id=current_user.id,
            skill_id=skill_id,
            level=level
        )
        db.session.add(new_skill)
    
    db.session.commit()
    flash('Skill updated successfully!')
    return redirect(url_for('user.profile'))

@user_bp.route('/remove-skill/<int:skill_id>')
@login_required
def remove_skill(skill_id):
    skill = UserSkill.query.filter_by(
        user_id=current_user.id,
        skill_id=skill_id
    ).first()
    
    if skill:
        db.session.delete(skill)
        db.session.commit()
        flash('Skill removed successfully!')
    
    return redirect(url_for('user.profile'))