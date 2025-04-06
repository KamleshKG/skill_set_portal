from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.services.project_service import ProjectService
from app.models.incident import Incident

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        abort(403)
    
    # Get project stats
    open_projects = Project.query.filter_by(status='open').count()
    closed_projects = Project.query.filter_by(status='closed').count()
    total_responses = Response.query.count()
    
    # Get recent incidents
    incidents = Incident.query.order_by(Incident.created_at.desc()).limit(5).all()
    
    # Get user activity
    active_users = User.query.order_by(User.last_login.desc()).limit(5).all()
    
    return render_template('dashboard/admin.html',
                         open_projects=open_projects,
                         closed_projects=closed_projects,
                         total_responses=total_responses,
                         incidents=incidents,
                         active_users=active_users)

@admin_bp.route('/incidents')
@login_required
def incident_list():
    if not current_user.is_admin:
        abort(403)
    
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    return render_template('incident/list.html', incidents=incidents)

@admin_bp.route('/restart-workflow/<workflow_id>')
@login_required
def restart_workflow(workflow_id):
    if not current_user.is_admin:
        abort(403)
    
    parts = workflow_id.split('_')
    if len(parts) != 2:
        abort(400)
    
    workflow_type, entity_id = parts
    success = ProjectService.restart_project_workflow(entity_id)
    
    if success:
        flash('Workflow restarted successfully', 'success')
    else:
        flash('Failed to restart workflow', 'danger')
    
    return redirect(url_for('admin.dashboard'))