import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    
    # Database configuration - Force in-memory SQLite for Render deployment
    if os.environ.get('DATABASE_URL'):
        # Production database (PostgreSQL on Render)
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
    elif os.environ.get('PORT'):  # Render sets PORT environment variable
        # Production on Render - use in-memory SQLite (temporary)
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    else:
        # Development database (SQLite)
        db_path = os.path.join(os.path.dirname(__file__), 'instance', 'churn_app.db')
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
    # Model paths - relative to backend folder
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'churn_model.pkl')
    SCALER_PATH = os.path.join(os.path.dirname(__file__), 'scaler.pkl')
    
    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@churnpredict.com'
    
    # Email Templates
    COMPANY_NAME = "ChurnPredict India"
    COMPANY_EMAIL = "support@churnpredict.com"