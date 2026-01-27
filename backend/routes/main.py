from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_login import login_required, current_user
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import csv
import io

from models import db, User, Prediction, ModelMetrics
from forms import PredictionForm
from ml_utils import predictor
from email_utils import send_prediction_email, send_bulk_prediction_email

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    user_stats = None
    if current_user.is_authenticated:
        user_stats = get_user_stats(current_user.id)
    return render_template('index.html', user_stats=user_stats)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Get user statistics
    stats = get_user_stats(current_user.id)
    
    # Get recent predictions
    recent_predictions = Prediction.query.filter_by(user_id=current_user.id)\
        .order_by(desc(Prediction.created_at)).limit(5).all()
    
    # Get model metrics
    model_metrics = ModelMetrics.get_latest()
    
    return render_template('dashboard.html', 
                         stats=stats, 
                         recent_predictions=recent_predictions,
                         model_metrics=model_metrics)
@main_bp.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    form = PredictionForm()
    prediction_result = None
    
    if form.validate_on_submit():
        try:
            # Make prediction
            prediction, probability = predictor.predict(
                tenure=form.tenure.data,
                monthly_charges=form.monthly_charges.data,
                total_charges=form.total_charges.data,
                contract_type=form.contract_type.data,
                payment_method=form.payment_method.data
            )
            
            # Save prediction to database
            pred_record = Prediction(
                user_id=current_user.id,
                customer_name=form.customer_name.data,
                tenure=form.tenure.data,
                monthly_charges=form.monthly_charges.data,
                total_charges=form.total_charges.data,
                contract_type=form.contract_type.data,
                payment_method=form.payment_method.data,
                prediction=prediction,
                probability=probability
            )
            
            # Calculate risk score (0-100)
            pred_record.calculate_risk_score()
            
            db.session.add(pred_record)
            db.session.commit()
            
            prediction_result = {
                'prediction': prediction,
                'probability': probability,
                'risk_score': pred_record.risk_score,
                'prediction_id': pred_record.id
            }
            
            flash('Prediction completed successfully!', 'success')
            
        except Exception as e:
            flash(f'Error making prediction: {str(e)}', 'error')
    
    return render_template('predict.html', form=form, prediction_result=prediction_result)

@main_bp.route('/send-prediction-email', methods=['POST'])
@login_required
def send_prediction_email_route():
    """Send prediction result via email"""
    try:
        prediction_id = request.form.get('prediction_id')
        recipient_email = request.form.get('recipient_email')
        sender_name = request.form.get('sender_name', current_user.username)
        
        if not prediction_id or not recipient_email:
            flash('Missing required information for sending email', 'error')
            return redirect(url_for('main.predict'))
        
        # Get prediction from database
        prediction = Prediction.query.filter_by(id=prediction_id, user_id=current_user.id).first()
        if not prediction:
            flash('Prediction not found', 'error')
            return redirect(url_for('main.predict'))
        
        # Prepare prediction data
        prediction_data = {
            'prediction': prediction.prediction,
            'probability': prediction.probability,
            'tenure': prediction.tenure,
            'monthly_charges': prediction.monthly_charges,
            'total_charges': prediction.total_charges,
            'contract_type': prediction.contract_type,
            'payment_method': prediction.payment_method,
            'internet_service': getattr(prediction, 'internet_service', 'N/A')
        }
        
        # Send email
        success = send_prediction_email(
            recipient_email=recipient_email,
            customer_name=prediction.customer_name,
            prediction_data=prediction_data,
            sender_name=sender_name
        )
        
        if success:
            flash(f'Prediction report sent successfully to {recipient_email}!', 'success')
        else:
            flash('Failed to send email. Please check the email address and try again.', 'error')
        
    except Exception as e:
        flash(f'Error sending email: {str(e)}', 'error')
    
    return redirect(url_for('main.predict'))

@main_bp.route('/bulk-predict', methods=['GET', 'POST'])
@login_required
def bulk_predict():
    """Bulk prediction from CSV file"""
    results = []
    error_count = 0
    success_count = 0
    
    if request.method == 'POST':
        # Check if file is in request
        if 'csv_file' not in request.files:
            flash('No file provided', 'error')
            return render_template('bulk_predict.html', results=[], success_count=0, error_count=0)
        
        file = request.files['csv_file']
        
        if file.filename == '':
            flash('No file selected', 'error')
            return render_template('bulk_predict.html', results=[], success_count=0, error_count=0)
        
        if not file.filename.endswith('.csv'):
            flash('Please upload a CSV file', 'error')
            return render_template('bulk_predict.html', results=[], success_count=0, error_count=0)
        
        try:
            # Parse CSV file
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_reader = csv.DictReader(stream)
            
            for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 (accounting for header)
                try:
                    # Extract data from CSV
                    customer_name = row.get('customer_name', f'Customer {row_num}')
                    tenure = float(row.get('tenure', 0))
                    monthly_charges = float(row.get('monthly_charges', 0))
                    total_charges = float(row.get('total_charges', 0))
                    contract_type = row.get('contract_type', 'Month-to-month')
                    payment_method = row.get('payment_method', 'Electronic check')
                    
                    # Make prediction
                    prediction, probability = predictor.predict(
                        tenure=tenure,
                        monthly_charges=monthly_charges,
                        total_charges=total_charges,
                        contract_type=contract_type,
                        payment_method=payment_method
                    )
                    
                    # Save to database
                    pred_record = Prediction(
                        user_id=current_user.id,
                        customer_name=customer_name,
                        tenure=tenure,
                        monthly_charges=monthly_charges,
                        total_charges=total_charges,
                        contract_type=contract_type,
                        payment_method=payment_method,
                        prediction=prediction,
                        probability=probability
                    )
                    
                    pred_record.calculate_risk_score()
                    db.session.add(pred_record)
                    
                    results.append({
                        'row': row_num,
                        'name': customer_name,
                        'status': 'success',
                        'prediction': 'Churn' if prediction == 1 else 'No Churn',
                        'risk_score': pred_record.risk_score,
                        'probability': f"{probability:.1%}"
                    })
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    results.append({
                        'row': row_num,
                        'name': row.get('customer_name', 'Unknown'),
                        'status': 'error',
                        'error': str(e)
                    })
            
            # Commit all predictions
            if success_count > 0:
                db.session.commit()
                flash(f'Successfully imported {success_count} predictions!', 'success')
            
            if error_count > 0:
                flash(f'Failed to import {error_count} records. Check the details below.', 'warning')
        
        except Exception as e:
            flash(f'Error processing CSV file: {str(e)}', 'error')
    
    return render_template('bulk_predict.html', results=results, success_count=success_count, error_count=error_count)

@main_bp.route('/send-bulk-email', methods=['POST'])
@login_required
def send_bulk_email():
    """Send bulk prediction results via email"""
    try:
        recipient_email = request.form.get('recipient_email')
        sender_name = request.form.get('sender_name', current_user.username)
        
        if not recipient_email:
            flash('Email address is required', 'error')
            return redirect(url_for('main.bulk_predict'))
        
        # Get recent predictions (last 50 for email)
        predictions = Prediction.query.filter_by(user_id=current_user.id)\
            .order_by(desc(Prediction.created_at)).limit(50).all()
        
        if not predictions:
            flash('No predictions found to send', 'error')
            return redirect(url_for('main.bulk_predict'))
        
        # Prepare predictions data
        predictions_data = []
        for pred in predictions:
            predictions_data.append({
                'customer_name': pred.customer_name,
                'prediction': pred.prediction,
                'probability': pred.probability,
                'tenure': pred.tenure,
                'monthly_charges': pred.monthly_charges,
                'total_charges': pred.total_charges,
                'contract_type': pred.contract_type,
                'payment_method': pred.payment_method
            })
        
        # Send email
        success = send_bulk_prediction_email(
            recipient_email=recipient_email,
            predictions_data=predictions_data,
            sender_name=sender_name
        )
        
        if success:
            flash(f'Bulk prediction report sent successfully to {recipient_email}!', 'success')
        else:
            flash('Failed to send email. Please check the email address and try again.', 'error')
        
    except Exception as e:
        flash(f'Error sending bulk email: {str(e)}', 'error')
    
    return redirect(url_for('main.bulk_predict'))

@main_bp.route('/history')
@login_required
def history():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10
        
        # Ensure page is at least 1
        if page < 1:
            page = 1
        
        # Build query with filters
        query = Prediction.query.filter_by(user_id=current_user.id)
        
        # Filter by prediction type
        prediction_filter = request.args.get('prediction_filter')
        if prediction_filter in ['0', '1']:
            query = query.filter(Prediction.prediction == int(prediction_filter))
        
        # Filter by date range
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        
        if from_date:
            try:
                from_date = datetime.strptime(from_date, '%Y-%m-%d')
                query = query.filter(Prediction.created_at >= from_date)
            except ValueError:
                flash('Invalid from date format', 'warning')
        
        if to_date:
            try:
                to_date = datetime.strptime(to_date, '%Y-%m-%d') + timedelta(days=1)
                query = query.filter(Prediction.created_at < to_date)
            except ValueError:
                flash('Invalid to date format', 'warning')
        
        # Check for CSV export
        if request.args.get('export') == 'csv':
            return export_predictions_csv(query.all())
        
        # Get total count before pagination
        total_count = query.count()
        
        # Calculate max page
        max_page = (total_count + per_page - 1) // per_page if total_count > 0 else 1
        
        # If page is beyond max page, redirect to last page
        if page > max_page and total_count > 0:
            return redirect(url_for('main.history', page=max_page, **{k: v for k, v in request.args.items() if k != 'page'}))
        
        # Paginate results
        predictions = query.order_by(desc(Prediction.created_at))\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        # Debug info (remove in production)
        print(f"DEBUG: History page {page}, total items: {predictions.total}, pages: {predictions.pages}")
        
        # If no items and not on page 1, redirect to page 1
        if not predictions.items and page > 1:
            print(f"DEBUG: No items on page {page}, redirecting to page 1")
            return redirect(url_for('main.history', page=1, **{k: v for k, v in request.args.items() if k != 'page'}))
        
        return render_template('history.html', predictions=predictions)
        
    except Exception as e:
        flash(f'Error loading prediction history: {str(e)}', 'error')
        # Redirect to page 1 on any error
        return redirect(url_for('main.history', page=1))

@main_bp.route('/export-email', methods=['POST'])
@login_required
def export_email():
    """Export prediction history as CSV and show download option"""
    try:
        # Get user's predictions
        predictions = Prediction.query.filter_by(user_id=current_user.id)\
            .order_by(desc(Prediction.created_at)).all()
        
        if not predictions:
            flash('No predictions to export', 'warning')
            return redirect(url_for('main.history'))
        
        # Generate CSV content
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Customer Name', 'Tenure (Months)', 'Monthly Charges (₹)', 'Total Charges (₹)',
            'Contract Type', 'Payment Method', 'Prediction', 'Risk Score', 'Probability', 'Date'
        ])
        
        # Write data
        for pred in predictions:
            writer.writerow([
                pred.customer_name,
                f"{pred.tenure} months",
                f"₹{pred.monthly_charges:,.0f}",
                f"₹{pred.total_charges:,.0f}",
                pred.contract_type,
                pred.payment_method,
                'Churn' if pred.prediction == 1 else 'No Churn',
                pred.risk_score,
                f"{pred.probability:.3f}",
                pred.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        output.seek(0)
        
        # Create response
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename=churn_predictions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        flash(f'Export ready! Downloaded {len(predictions)} predictions.', 'success')
        return response
        
    except Exception as e:
        flash(f'Error exporting predictions: {str(e)}', 'error')
        return redirect(url_for('main.history'))

@main_bp.route('/settings')
@login_required
def settings():
    user_stats = get_user_stats(current_user.id)
    return render_template('settings.html', user_stats=user_stats)
@main_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not current_user.check_password(current_password):
        flash('Current password is incorrect.', 'error')
        return redirect(url_for('main.settings'))
    
    if new_password != confirm_password:
        flash('New passwords do not match.', 'error')
        return redirect(url_for('main.settings'))
    
    if len(new_password) < 6:
        flash('Password must be at least 6 characters long.', 'error')
        return redirect(url_for('main.settings'))
    
    current_user.set_password(new_password)
    db.session.commit()
    
    flash('Password updated successfully!', 'success')
    return redirect(url_for('main.settings'))

@main_bp.route('/export-data')
@login_required
def export_data():
    predictions = Prediction.query.filter_by(user_id=current_user.id).all()
    return export_predictions_csv(predictions)

@main_bp.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    username_confirm = request.form.get('username_confirm')
    
    if username_confirm != current_user.username:
        flash('Username confirmation does not match.', 'error')
        return redirect(url_for('main.settings'))
    
    # Delete all user predictions
    Prediction.query.filter_by(user_id=current_user.id).delete()
    
    # Delete user account
    db.session.delete(current_user)
    db.session.commit()
    
    flash('Your account has been deleted successfully.', 'info')
    return redirect(url_for('main.index'))

def get_user_stats(user_id):
    """Get user statistics"""
    predictions = Prediction.query.filter_by(user_id=user_id).all()
    
    total_predictions = len(predictions)
    churn_predictions = sum(1 for p in predictions if p.prediction == 1)
    no_churn_predictions = total_predictions - churn_predictions
    avg_probability = sum(p.probability for p in predictions) / total_predictions if total_predictions > 0 else 0
    
    return {
        'total_predictions': total_predictions,
        'churn_predictions': churn_predictions,
        'no_churn_predictions': no_churn_predictions,
        'avg_probability': avg_probability
    }

def export_predictions_csv(predictions):
    """Export predictions to CSV with Indian formatting"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Customer Name', 'Tenure (Months)', 'Monthly Charges (₹)', 'Total Charges (₹)',
        'Contract Type', 'Payment Method', 'Prediction', 'Probability', 'Date'
    ])
    
    # Write data
    for pred in predictions:
        writer.writerow([
            pred.customer_name,
            f"{pred.tenure} months",
            f"₹{pred.monthly_charges:,.0f}",
            f"₹{pred.total_charges:,.0f}",
            pred.contract_type,
            pred.payment_method,
            'Churn' if pred.prediction == 1 else 'No Churn',
            f"{pred.probability:.3f}",
            pred.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    output.seek(0)
    
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=churn_predictions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    return response