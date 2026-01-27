#!/usr/bin/env python3
"""
Initialize Indian Demo Data for Customer Churn Prediction System
Demo data initialization script with Indian business context and ₹ currency
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)

from app_flask import create_app
from models import db, User, Prediction, ModelMetrics

def create_indian_users():
    """Create Indian demo users"""
    users_data = [
        {
            'username': 'admin',
            'email': 'admin@churnpredict.in',
            'password': 'admin123',
            'role': 'admin'
        },
        {
            'username': 'demo_user',
            'email': 'demo@churnpredict.in',
            'password': 'user123',
            'role': 'user'
        },
        {
            'username': 'rajesh_kumar',
            'email': 'rajesh.kumar@example.in',
            'password': 'demo123',
            'role': 'user'
        },
        {
            'username': 'priya_sharma',
            'email': 'priya.sharma@example.in',
            'password': 'demo123',
            'role': 'user'
        },
        {
            'username': 'amit_gupta',
            'email': 'amit.gupta@example.in',
            'password': 'demo123',
            'role': 'user'
        }
    ]
    
    created_users = []
    for user_data in users_data:
        # Check if user already exists
        existing_user = User.query.filter_by(username=user_data['username']).first()
        if not existing_user:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                role=user_data['role']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
            created_users.append(user)
            print(f"✅ Created user: {user_data['username']}")
        else:
            created_users.append(existing_user)
            print(f"ℹ️  User already exists: {user_data['username']}")
    
    db.session.commit()
    return created_users

def create_indian_predictions():
    """Create Indian demo predictions with realistic data"""
    
    # Get demo user
    demo_user = User.query.filter_by(username='demo_user').first()
    if not demo_user:
        print("❌ Demo user not found!")
        return
    
    # Indian customer names and realistic data
    indian_customers = [
        # High churn risk customers
        {
            'name': 'Rajesh Kumar',
            'tenure': 2,
            'monthly_charges': 2500,
            'total_charges': 5000,
            'contract_type': 'Month-to-month',
            'payment_method': 'Electronic check',
            'prediction': 1,
            'probability': 0.87
        },
        {
            'name': 'Amit Gupta',
            'tenure': 1,
            'monthly_charges': 3200,
            'total_charges': 3200,
            'contract_type': 'Month-to-month',
            'payment_method': 'Electronic check',
            'prediction': 1,
            'probability': 0.92
        },
        {
            'name': 'Suresh Yadav',
            'tenure': 3,
            'monthly_charges': 2800,
            'total_charges': 8400,
            'contract_type': 'Month-to-month',
            'payment_method': 'Mailed check',
            'prediction': 1,
            'probability': 0.78
        },
        {
            'name': 'Rohit Singh',
            'tenure': 2,
            'monthly_charges': 1999,
            'total_charges': 3998,
            'contract_type': 'Month-to-month',
            'payment_method': 'Electronic check',
            'prediction': 1,
            'probability': 0.83
        },
        
        # Low churn risk customers  
        {
            'name': 'Priya Sharma',
            'tenure': 36,
            'monthly_charges': 1950,
            'total_charges': 70200,
            'contract_type': 'Two year',
            'payment_method': 'UPI',
            'prediction': 0,
            'probability': 0.15
        },
        {
            'name': 'Anita Singh',
            'tenure': 24,
            'monthly_charges': 1200,
            'total_charges': 28800,
            'contract_type': 'One year',
            'payment_method': 'Net Banking',
            'prediction': 0,
            'probability': 0.22
        },
        {
            'name': 'Vikas Agarwal',
            'tenure': 18,
            'monthly_charges': 899,
            'total_charges': 16182,
            'contract_type': 'One year',
            'payment_method': 'Credit card (automatic)',
            'prediction': 0,
            'probability': 0.18
        },
        {
            'name': 'Sunita Devi',
            'tenure': 42,
            'monthly_charges': 799,
            'total_charges': 33558,
            'contract_type': 'Two year',
            'payment_method': 'UPI',
            'prediction': 0,
            'probability': 0.12
        },
        {
            'name': 'Manish Kumar',
            'tenure': 30,
            'monthly_charges': 1499,
            'total_charges': 44970,
            'contract_type': 'Two year',
            'payment_method': 'Digital Wallet',
            'prediction': 0,
            'probability': 0.19
        },
        
        # Medium risk customers
        {
            'name': 'Rohit Verma',
            'tenure': 8,
            'monthly_charges': 1599,
            'total_charges': 12792,
            'contract_type': 'Month-to-month',
            'payment_method': 'Net Banking',
            'prediction': 0,
            'probability': 0.45
        },
        {
            'name': 'Meera Joshi',
            'tenure': 6,
            'monthly_charges': 1899,
            'total_charges': 11394,
            'contract_type': 'One year',
            'payment_method': 'Digital Wallet',
            'prediction': 0,
            'probability': 0.38
        },
        {
            'name': 'Arun Kumar',
            'tenure': 12,
            'monthly_charges': 1299,
            'total_charges': 15588,
            'contract_type': 'One year',
            'payment_method': 'UPI',
            'prediction': 0,
            'probability': 0.35
        },
        {
            'name': 'Kavita Patel',
            'tenure': 9,
            'monthly_charges': 1799,
            'total_charges': 16191,
            'contract_type': 'Month-to-month',
            'payment_method': 'Credit card (automatic)',
            'prediction': 0,
            'probability': 0.42
        },
        {
            'name': 'Sanjay Mehta',
            'tenure': 15,
            'monthly_charges': 999,
            'total_charges': 14985,
            'contract_type': 'One year',
            'payment_method': 'Net Banking',
            'prediction': 0,
            'probability': 0.28
        }
    ]
    
    created_count = 0
    for customer in indian_customers:
        # Create prediction with some date variation
        days_ago = random.randint(1, 90)
        created_at = datetime.utcnow() - timedelta(days=days_ago)
        
        prediction = Prediction(
            user_id=demo_user.id,
            customer_name=customer['name'],
            tenure=customer['tenure'],
            monthly_charges=customer['monthly_charges'],
            total_charges=customer['total_charges'],
            contract_type=customer['contract_type'],
            payment_method=customer['payment_method'],
            prediction=customer['prediction'],
            probability=customer['probability'],
            created_at=created_at
        )
        
        db.session.add(prediction)
        created_count += 1
    
    db.session.commit()
    print(f"✅ Created {created_count} Indian demo predictions")

def create_model_metrics():
    """Create model performance metrics"""
    # Check if metrics already exist
    existing_metrics = ModelMetrics.query.first()
    if not existing_metrics:
        metrics = ModelMetrics(
            accuracy=0.85,
            precision=0.82,
            recall=0.78,
            f1_score=0.80
        )
        db.session.add(metrics)
        db.session.commit()
        print("✅ Created model metrics")
    else:
        print("ℹ️  Model metrics already exist")

def main():
    """Main initialization function"""
    print("🇮🇳 Initializing Indian Demo Data...")
    print("=" * 50)
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
        # Create users
        print("\n👥 Creating Indian demo users...")
        users = create_indian_users()
        
        # Create predictions
        print("\n📊 Creating Indian demo predictions...")
        create_indian_predictions()
        
        # Create model metrics
        print("\n🎯 Creating model metrics...")
        create_model_metrics()
        
        print("\n" + "=" * 50)
        print("🎉 Indian demo data initialization completed!")
        print("=" * 50)
        
        print("\n📋 Demo Accounts:")
        print("   Admin: admin / admin123")
        print("   User:  demo_user / user123")
        print("   Indian Users: rajesh_kumar, priya_sharma / demo123")
        
        print("\n🚀 Start the application with:")
        print("   python run.py")
        
        print("\n🌐 Then visit: http://localhost:5000")

if __name__ == "__main__":
    main()