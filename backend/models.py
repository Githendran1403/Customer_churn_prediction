from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import bcrypt

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user')  # 'admin' or 'user'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship with predictions
    predictions = db.relationship('Prediction', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def is_admin(self):
        return self.role == 'admin'

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Customer features
    tenure = db.Column(db.Float, nullable=False)
    monthly_charges = db.Column(db.Float, nullable=False)
    total_charges = db.Column(db.Float, nullable=False)
    contract_type = db.Column(db.String(50), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    
    # Prediction results
    prediction = db.Column(db.Integer, nullable=False)  # 0 or 1
    probability = db.Column(db.Float, nullable=False)
    risk_score = db.Column(db.Integer, nullable=False, default=0)  # 0-100 risk score
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    customer_name = db.Column(db.String(100))
    
    def calculate_risk_score(self):
        """Calculate risk score from 0-100 based on churn probability"""
        self.risk_score = int(self.probability * 100)
        return self.risk_score
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'tenure': self.tenure,
            'monthly_charges': self.monthly_charges,
            'total_charges': self.total_charges,
            'contract_type': self.contract_type,
            'payment_method': self.payment_method,
            'prediction': self.prediction,
            'probability': self.probability,
            'risk_score': self.risk_score,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class ModelMetrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accuracy = db.Column(db.Float, nullable=False)
    precision = db.Column(db.Float, nullable=False)
    recall = db.Column(db.Float, nullable=False)
    f1_score = db.Column(db.Float, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @classmethod
    def get_latest(cls):
        return cls.query.order_by(cls.updated_at.desc()).first()