"""
Email utility functions for sending prediction results
"""

from flask import current_app, render_template_string
from flask_mail import Message
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def send_prediction_email(recipient_email, customer_name, prediction_data, sender_name=None):
    """
    Send prediction results via email
    
    Args:
        recipient_email (str): Email address to send to
        customer_name (str): Name of the customer being predicted
        prediction_data (dict): Prediction results and customer data
        sender_name (str): Name of the person sending the email
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        from app_flask import mail
        
        # Create email subject
        prediction_text = "Likely to Churn" if prediction_data['prediction'] == 1 else "Not Likely to Churn"
        subject = f"Customer Churn Prediction Report - {customer_name}"
        
        # Create email body
        html_body = create_prediction_email_template(
            customer_name=customer_name,
            prediction_data=prediction_data,
            sender_name=sender_name
        )
        
        # Create message
        msg = Message(
            subject=subject,
            recipients=[recipient_email],
            html=html_body,
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        
        # Send email
        mail.send(msg)
        logger.info(f"Prediction email sent successfully to {recipient_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send prediction email to {recipient_email}: {str(e)}")
        return False

def send_bulk_prediction_email(recipient_email, predictions_data, sender_name=None):
    """
    Send bulk prediction results via email
    
    Args:
        recipient_email (str): Email address to send to
        predictions_data (list): List of prediction results
        sender_name (str): Name of the person sending the email
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        from app_flask import mail
        
        # Create email subject
        total_predictions = len(predictions_data)
        churn_count = sum(1 for p in predictions_data if p['prediction'] == 1)
        subject = f"Bulk Churn Prediction Report - {total_predictions} Customers Analyzed"
        
        # Create email body
        html_body = create_bulk_prediction_email_template(
            predictions_data=predictions_data,
            sender_name=sender_name,
            total_predictions=total_predictions,
            churn_count=churn_count
        )
        
        # Create message
        msg = Message(
            subject=subject,
            recipients=[recipient_email],
            html=html_body,
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        
        # Send email
        mail.send(msg)
        logger.info(f"Bulk prediction email sent successfully to {recipient_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send bulk prediction email to {recipient_email}: {str(e)}")
        return False

def create_prediction_email_template(customer_name, prediction_data, sender_name=None):
    """Create HTML email template for single prediction"""
    
    prediction_text = "Likely to Churn" if prediction_data['prediction'] == 1 else "Not Likely to Churn"
    prediction_color = "#dc2626" if prediction_data['prediction'] == 1 else "#10b981"
    probability_percent = round(prediction_data['probability'] * 100, 1)
    
    # Format currency values
    monthly_charges = f"₹{prediction_data['monthly_charges']:,.0f}"
    total_charges = f"₹{prediction_data['total_charges']:,.0f}"
    
    template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Customer Churn Prediction Report</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f8fafc; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
            .header {{ background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ padding: 30px; }}
            .prediction-result {{ text-align: center; padding: 20px; margin: 20px 0; border-radius: 8px; border: 2px solid {prediction_color}; background-color: {prediction_color}15; }}
            .prediction-text {{ font-size: 24px; font-weight: bold; color: {prediction_color}; margin-bottom: 10px; }}
            .probability {{ font-size: 18px; color: #64748b; }}
            .details-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            .details-table th, .details-table td {{ padding: 12px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
            .details-table th {{ background-color: #f1f5f9; font-weight: 600; }}
            .footer {{ background-color: #f8fafc; padding: 20px; text-align: center; border-radius: 0 0 8px 8px; color: #64748b; font-size: 14px; }}
            .logo {{ font-size: 28px; font-weight: bold; margin-bottom: 10px; }}
            .tagline {{ font-size: 16px; opacity: 0.9; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">📊 ChurnPredict India</div>
                <div class="tagline">AI-Powered Customer Retention Analytics</div>
            </div>
            
            <div class="content">
                <h2>Customer Churn Prediction Report</h2>
                
                <div class="prediction-result">
                    <div class="prediction-text">{prediction_text}</div>
                    <div class="probability">Churn Probability: {probability_percent}%</div>
                </div>
                
                <h3>Customer Details</h3>
                <table class="details-table">
                    <tr>
                        <th>Customer Name</th>
                        <td>{customer_name}</td>
                    </tr>
                    <tr>
                        <th>Tenure</th>
                        <td>{prediction_data['tenure']} months</td>
                    </tr>
                    <tr>
                        <th>Monthly Charges</th>
                        <td>{monthly_charges}</td>
                    </tr>
                    <tr>
                        <th>Total Charges</th>
                        <td>{total_charges}</td>
                    </tr>
                    <tr>
                        <th>Contract Type</th>
                        <td>{prediction_data['contract_type']}</td>
                    </tr>
                    <tr>
                        <th>Payment Method</th>
                        <td>{prediction_data['payment_method']}</td>
                    </tr>
                    <tr>
                        <th>Internet Service</th>
                        <td>{prediction_data.get('internet_service', 'N/A')}</td>
                    </tr>
                </table>
                
                <div style="background-color: #eff6ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h4 style="color: #1e40af; margin-top: 0;">💡 Recommendations</h4>
                    <ul style="color: #374151; line-height: 1.6;">
                        {"<li>High churn risk - Consider immediate retention strategies</li><li>Offer personalized discounts or service upgrades</li><li>Schedule a customer satisfaction call</li><li>Review contract terms and payment options</li>" if prediction_data['prediction'] == 1 else "<li>Low churn risk - Customer appears satisfied</li><li>Continue providing excellent service</li><li>Consider upselling opportunities</li><li>Use as a reference for best practices</li>"}
                    </ul>
                </div>
                
                {"<p><strong>Sent by:</strong> " + sender_name + "</p>" if sender_name else ""}
                <p><strong>Generated on:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
            
            <div class="footer">
                <p>This report was generated by ChurnPredict India's AI-powered analytics platform.</p>
                <p>For support, contact us at support@churnpredict.com</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return template

def create_bulk_prediction_email_template(predictions_data, sender_name, total_predictions, churn_count):
    """Create HTML email template for bulk predictions"""
    
    no_churn_count = total_predictions - churn_count
    churn_percentage = round((churn_count / total_predictions) * 100, 1) if total_predictions > 0 else 0
    
    # Create table rows for predictions
    table_rows = ""
    for i, pred in enumerate(predictions_data[:20]):  # Limit to first 20 for email
        prediction_text = "Churn" if pred['prediction'] == 1 else "No Churn"
        color = "#dc2626" if pred['prediction'] == 1 else "#10b981"
        probability = round(pred['probability'] * 100, 1)
        monthly_charges = f"₹{pred['monthly_charges']:,.0f}"
        
        table_rows += f"""
        <tr>
            <td>{i+1}</td>
            <td>{pred['customer_name']}</td>
            <td><span style="color: {color}; font-weight: bold;">{prediction_text}</span></td>
            <td>{probability}%</td>
            <td>{pred['tenure']} months</td>
            <td>{monthly_charges}</td>
        </tr>
        """
    
    if total_predictions > 20:
        table_rows += f"""
        <tr style="background-color: #f8fafc;">
            <td colspan="6" style="text-align: center; font-style: italic; color: #64748b;">
                ... and {total_predictions - 20} more customers
            </td>
        </tr>
        """
    
    template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bulk Customer Churn Prediction Report</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f8fafc; }}
            .container {{ max-width: 800px; margin: 0 auto; background-color: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
            .header {{ background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ padding: 30px; }}
            .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
            .stat-card {{ text-align: center; padding: 20px; border-radius: 8px; background-color: #f8fafc; }}
            .stat-number {{ font-size: 32px; font-weight: bold; margin-bottom: 5px; }}
            .stat-label {{ color: #64748b; font-size: 14px; }}
            .predictions-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            .predictions-table th, .predictions-table td {{ padding: 12px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
            .predictions-table th {{ background-color: #f1f5f9; font-weight: 600; }}
            .footer {{ background-color: #f8fafc; padding: 20px; text-align: center; border-radius: 0 0 8px 8px; color: #64748b; font-size: 14px; }}
            .logo {{ font-size: 28px; font-weight: bold; margin-bottom: 10px; }}
            .tagline {{ font-size: 16px; opacity: 0.9; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">📊 ChurnPredict India</div>
                <div class="tagline">AI-Powered Customer Retention Analytics</div>
            </div>
            
            <div class="content">
                <h2>Bulk Customer Churn Prediction Report</h2>
                
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number" style="color: #2563eb;">{total_predictions}</div>
                        <div class="stat-label">Total Customers</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" style="color: #dc2626;">{churn_count}</div>
                        <div class="stat-label">Likely to Churn</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" style="color: #10b981;">{no_churn_count}</div>
                        <div class="stat-label">Not Likely to Churn</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" style="color: #f59e0b;">{churn_percentage}%</div>
                        <div class="stat-label">Churn Rate</div>
                    </div>
                </div>
                
                <h3>Prediction Results</h3>
                <table class="predictions-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Customer Name</th>
                            <th>Prediction</th>
                            <th>Probability</th>
                            <th>Tenure</th>
                            <th>Monthly Charges</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
                
                <div style="background-color: #eff6ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h4 style="color: #1e40af; margin-top: 0;">📈 Summary & Recommendations</h4>
                    <ul style="color: #374151; line-height: 1.6;">
                        <li><strong>Churn Rate:</strong> {churn_percentage}% of analyzed customers are at risk</li>
                        <li><strong>Priority Action:</strong> Focus on the {churn_count} high-risk customers immediately</li>
                        <li><strong>Retention Strategy:</strong> Implement targeted campaigns for at-risk customers</li>
                        <li><strong>Success Metrics:</strong> Monitor the {no_churn_count} satisfied customers for best practices</li>
                    </ul>
                </div>
                
                {"<p><strong>Sent by:</strong> " + sender_name + "</p>" if sender_name else ""}
                <p><strong>Generated on:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
            
            <div class="footer">
                <p>This report was generated by ChurnPredict India's AI-powered analytics platform.</p>
                <p>For support, contact us at support@churnpredict.com</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return template