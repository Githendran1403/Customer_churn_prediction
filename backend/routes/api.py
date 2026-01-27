from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy import func, desc
from datetime import datetime, timedelta

from models import db, Prediction

api_bp = Blueprint('api', __name__)

@api_bp.route('/prediction/<int:prediction_id>')
@login_required
def get_prediction(prediction_id):
    prediction = Prediction.query.get_or_404(prediction_id)
    
    # Check if user owns this prediction or is admin
    if prediction.user_id != current_user.id and not current_user.is_admin():
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify(prediction.to_dict())

@api_bp.route('/prediction/<int:prediction_id>', methods=['DELETE'])
@login_required
def delete_prediction(prediction_id):
    prediction = Prediction.query.get_or_404(prediction_id)
    
    # Check if user owns this prediction or is admin
    if prediction.user_id != current_user.id and not current_user.is_admin():
        return jsonify({'error': 'Access denied'}), 403
    
    db.session.delete(prediction)
    db.session.commit()
    
    return jsonify({'success': True})

@api_bp.route('/prediction-stats')
@login_required
def prediction_stats():
    # Get user's prediction statistics
    predictions = Prediction.query.filter_by(user_id=current_user.id).all()
    
    churn_count = sum(1 for p in predictions if p.prediction == 1)
    no_churn_count = len(predictions) - churn_count
    
    return jsonify({
        'churn': churn_count,
        'no_churn': no_churn_count
    })

@api_bp.route('/monthly-trend')
@login_required
def monthly_trend():
    # Get user's predictions for the last 12 months
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=365)
    
    # Query predictions by month
    predictions = db.session.query(
        func.strftime('%Y-%m', Prediction.created_at).label('month'),
        func.count(Prediction.id).label('count')
    ).filter(
        Prediction.user_id == current_user.id,
        Prediction.created_at >= start_date
    ).group_by(
        func.strftime('%Y-%m', Prediction.created_at)
    ).order_by('month').all()
    
    months = [pred.month for pred in predictions]
    counts = [pred.count for pred in predictions]
    
    return jsonify({
        'months': months,
        'counts': counts
    })