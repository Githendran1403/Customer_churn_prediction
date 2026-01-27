from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from functools import wraps
from sqlalchemy import func, desc
from datetime import datetime, timedelta

from models import db, User, Prediction, ModelMetrics

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # System statistics
    stats = {
        'total_users': User.query.count(),
        'active_users': User.query.filter_by(is_active=True).count(),
        'total_predictions': Prediction.query.count(),
        'churn_predictions': Prediction.query.filter_by(prediction=1).count()
    }
    
    # Get all users
    users = User.query.order_by(desc(User.created_at)).all()
    
    # Get model metrics
    model_metrics = ModelMetrics.get_latest()
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         users=users,
                         model_metrics=model_metrics)
@admin_bp.route('/create-user', methods=['POST'])
@login_required
@admin_required
def create_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')
    
    # Validation
    if User.query.filter_by(username=username).first():
        flash('Username already exists.', 'error')
        return redirect(url_for('admin.dashboard'))
    
    if User.query.filter_by(email=email).first():
        flash('Email already exists.', 'error')
        return redirect(url_for('admin.dashboard'))
    
    # Create user
    user = User(
        username=username,
        email=email,
        role=role
    )
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    flash(f'User {username} created successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

# API Routes for admin functionality
@admin_bp.route('/api/user/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        return jsonify({'success': False, 'message': 'Cannot modify your own status'})
    
    user.is_active = not user.is_active
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'status': 'active' if user.is_active else 'inactive'
    })

@admin_bp.route('/api/user/<int:user_id>', methods=['GET'])
@login_required
@admin_required
def get_user_details(user_id):
    user = User.query.get_or_404(user_id)
    
    # Get user statistics
    predictions = Prediction.query.filter_by(user_id=user_id).all()
    total_predictions = len(predictions)
    churn_predictions = sum(1 for p in predictions if p.prediction == 1)
    no_churn_predictions = total_predictions - churn_predictions
    avg_probability = sum(p.probability for p in predictions) / total_predictions if total_predictions > 0 else 0
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'is_active': user.is_active,
        'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'total_predictions': total_predictions,
        'churn_predictions': churn_predictions,
        'no_churn_predictions': no_churn_predictions,
        'avg_probability': avg_probability
    })

@admin_bp.route('/api/user/<int:user_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        return jsonify({'success': False, 'message': 'Cannot delete your own account'})
    
    # Delete user predictions first
    Prediction.query.filter_by(user_id=user_id).delete()
    
    # Delete user
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'success': True})

@admin_bp.route('/api/update-model-metrics', methods=['POST'])
@login_required
@admin_required
def update_model_metrics():
    # In a real application, you would recalculate these metrics
    # For demo purposes, we'll just update the timestamp
    metrics = ModelMetrics.get_latest()
    if metrics:
        metrics.updated_at = datetime.utcnow()
        db.session.commit()
    
    return jsonify({'success': True})

@admin_bp.route('/api/prediction-trends')
@login_required
@admin_required
def prediction_trends():
    try:
        # Get predictions for the last 30 days
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        print(f"DEBUG: Querying predictions from {start_date} to {end_date}")
        
        # Query predictions by date
        predictions = db.session.query(
            func.date(Prediction.created_at).label('date'),
            func.count(Prediction.id).label('count')
        ).filter(
            Prediction.created_at >= start_date
        ).group_by(
            func.date(Prediction.created_at)
        ).order_by('date').all()
        
        dates = [str(pred.date) for pred in predictions]
        counts = [pred.count for pred in predictions]
        
        print(f"DEBUG: Found {len(predictions)} date groups")
        print(f"DEBUG: Dates: {dates}")
        print(f"DEBUG: Counts: {counts}")
        
        result = {
            'dates': dates,
            'counts': counts
        }
        
        print(f"DEBUG: Returning JSON: {result}")
        return jsonify(result)
        
    except Exception as e:
        print(f"ERROR in prediction_trends: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'dates': [], 'counts': []})

@admin_bp.route('/api/user-activity')
@login_required
@admin_required
def user_activity():
    active_users = User.query.filter_by(is_active=True).count()
    inactive_users = User.query.filter_by(is_active=False).count()
    admin_users = User.query.filter_by(role='admin').count()
    
    return jsonify({
        'labels': ['Active Users', 'Inactive Users', 'Admin Users'],
        'values': [active_users, inactive_users, admin_users]
    })