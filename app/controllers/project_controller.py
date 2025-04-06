from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.project import Project, RequiredSkill, Response
from app.models.skill import Skill
from app.services.project_service import ProjectService

project_bp = Blueprint('project', __name__)

@project_bp.route('/projects')
@login_required
def list_projects():
    projects = ProjectService.get_projects_for_user(current_user.id)
    return render_template('project/list.html', projects=projects)

@project_bp.route('/projects/<int:project_id>')
@login_required
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    user_response = Response.query.filter_by(
        project_id=project_id,
        user_id=current_user.id
    ).first()
    return render_template('project/detail.html', 
                         project=project,
                         user_response=user_response)

@project_bp.route('/projects/create', methods=['GET', 'POST'])
@login_required
def create_project():
    if not current_user.is_admin:
        flash('Only admins can create projects', 'danger')
        return redirect(url_for('project.list_projects'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        skills = request.form.getlist('skills')
        levels = request.form.getlist('levels')
        
        required_skills = dict(zip(skills, levels))
        
        project = ProjectService.create_project(
            title=title,
            description=description,
            required_skills=required_skills,
            creator_id=current_user.id
        )
        
        flash('Project created successfully!', 'success')
        return redirect(url_for('project.project_detail', project_id=project.id))
    
    skills = Skill.query.all()
    return render_template('project/create.html', skills=skills)

@project_bp.route('/projects/<int:project_id>/respond', methods=['POST'])
@login_required
def respond_to_project(project_id):
    message = request.form.get('message')
    
    response = ProjectService.create_response(
        project_id=project_id,
        user_id=current_user.id,
        message=message
    )
    
    flash('Your response has been submitted', 'success')
    return redirect(url_for('project.project_detail', project_id=project_id))