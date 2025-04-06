from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('You need to be an admin to access this page', 'danger')
            return redirect(url_for('project.list_projects'))
        return f(*args, **kwargs)
    return decorated_function

def skill_required(skill_name, min_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            has_skill = any(
                us.skill.name == skill_name and us.level >= min_level
                for us in current_user.skills
            )
            if not has_skill:
                flash(f'You need {skill_name} skill (level {min_level}+) for this action', 'warning')
                return redirect(url_for('project.list_projects'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator