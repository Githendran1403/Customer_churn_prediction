from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import csv
import io
import os
from sqlalchemy import func, desc

from config import Config
from models import db, User, Prediction, ModelMetrics
from forms import LoginForm, RegistrationForm, PredictionForm
from ml_utils import predictor

# Global mail instance
mail = Mail()

def create_app():
    # Get the root directory (parent of backend)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    app = Flask(__name__, 
                template_folder=os.path.join(root_dir, 'frontend', 'templates'),
                static_folder=os.path.join(root_dir, 'frontend', 'static'))
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    
    # Login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create tables
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@churnpredict.in',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        # Create default user if not exists
        user = User.query.filter_by(username='demo_user').first()
        if not user:
            user = User(
                username='demo_user',
                email='demo@churnpredict.in',
                role='user'
            )
            user.set_password('user123')
            db.session.add(user)
        
        # Create default model metrics if not exists
        metrics = ModelMetrics.query.first()
        if not metrics:
            metrics = ModelMetrics(
                accuracy=0.85,
                precision=0.82,
                recall=0.78,
                f1_score=0.80
            )
            db.session.add(metrics)
        
        db.session.commit()
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.admin import admin_bp
    from routes.api import api_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Add test route for dark mode
    @app.route('/test-dark')
    def test_dark():
        return render_template('test_dark.html')
    
    # Add email demo route
    @app.route('/email-demo')
    def email_demo():
        return render_template('email_demo.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)