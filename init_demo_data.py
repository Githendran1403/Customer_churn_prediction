#!/usr/bin/env python3
"""
Initialize demo data for the Customer Churn Prediction System
"""

from app_flask import create_app
from models import db, User, Prediction, ModelMetrics
from ml_utils import predictor
import random
from datetime import datetime, timedelta

def create_demo_data():
    app = create_app()
    
    with app.app_context():
        print("🔄 Creating demo data...")
        
        # Get demo users
        admin = User.query.filter_by(username='admin').first()
        user = User.query.filter_by(username='user').first()
        
        if not admin or not user:
            print("❌ Demo users not found. Please run the app first to create them.")
            return
        
        # Sample customer data for predictions
        sample_customers = [
            {
                'name': 'John Smith',
                'tenure': 12,
                'monthly_charges': 75.50,
                'total_charges': 906.00,
                'contract_type': 'Month-to-month',
                'payment_method': 'Electronic check'
            },
            {
                'name': 'Sarah Johnson',
                'tenure': 36,
                'monthly_charges': 65.25,
                'total_charges': 2349.00,
                'contract_type': 'Two year',
                'payment_method': 'Credit card (automatic)'
            },
            {
                'name': 'Mike Davis',
                'tenure': 3,
                'monthly_charges': 89.99,
                'total_charges': 269.97,
                'contract_type': 'Month-to-month',
                'payment_method': 'Electronic check'
            },
            {
                'name': 'Emily Wilson',
                'tenure': 24,
                'monthly_charges': 55.75,
                'total_charges': 1338.00,
                'contract_type': 'One year',
                'payment_method': 'Bank transfer (automatic)'
            },
            {
                'name': 'Robert Brown',
                'tenure': 6,
                'monthly_charges': 95.00,
                'total_charges': 570.00,
                'contract_type': 'Month-to-month',
                'payment_method': 'Mailed check'
            }
        ]
        
        # Create demo predictions
        users_to_add_data = [user, admin]
        
        for demo_user in users_to_add_data:
            for i, customer in enumerate(sample_customers):
                try:
                    # Make prediction
                    prediction, probability = predictor.predict(
                        tenure=customer['tenure'],
                        monthly_charges=customer['monthly_charges'],
                        total_charges=customer['total_charges'],
                        contract_type=customer['contract_type'],
                        payment_method=customer['payment_method']
                    )
                    
                    # Create prediction record with random date in the past
                    days_ago = random.randint(1, 30)
                    created_at = datetime.utcnow() - timedelta(days=days_ago)
                    
                    pred_record = Prediction(
                        user_id=demo_user.id,
                        customer_name=customer['name'],
                        tenure=customer['tenure'],
                        monthly_charges=customer['monthly_charges'],
                        total_charges=customer['total_charges'],
                        contract_type=customer['contract_type'],
                        payment_method=customer['payment_method'],
                        prediction=prediction,
                        probability=probability,
                        created_at=created_at
                    )
                    
                    db.session.add(pred_record)
                    print(f"✅ Added prediction for {customer['name']} (User: {demo_user.username})")
                    
                except Exception as e:
                    print(f"❌ Error creating prediction for {customer['name']}: {e}")
        
        # Update model metrics with realistic values
        metrics = ModelMetrics.get_latest()
        if metrics:
            metrics.accuracy = 0.87
            metrics.precision = 0.84
            metrics.recall = 0.81
            metrics.f1_score = 0.82
            metrics.updated_at = datetime.utcnow()
            print("✅ Updated model metrics")
        
        db.session.commit()
        print("🎉 Demo data created successfully!")
        print("\n📊 You can now:")
        print("1. Login with demo credentials")
        print("2. View the dashboard with sample data")
        print("3. Explore prediction history")
        print("4. Test the admin panel")

if __name__ == '__main__':
    create_demo_data()