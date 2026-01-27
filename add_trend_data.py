#!/usr/bin/env python3
"""
Add more prediction data with better date distribution for trends
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)

from app_flask import create_app
from models import db, User, Prediction

def add_trend_data():
    """Add more predictions with better date distribution"""
    app = create_app()
    
    with app.app_context():
        print("📈 Adding prediction trend data...")
        print("=" * 50)
        
        # Get demo user
        demo_user = User.query.filter_by(username='demo_user').first()
        admin_user = User.query.filter_by(username='admin').first()
        
        if not demo_user or not admin_user:
            print("❌ Demo users not found!")
            return
        
        # Create predictions for each day in the last 30 days
        end_date = datetime.now()
        
        customers = [
            "Arjun Patel", "Sneha Reddy", "Vikram Singh", "Pooja Sharma", 
            "Rahul Kumar", "Anita Gupta", "Sanjay Mehta", "Kavita Joshi",
            "Deepak Agarwal", "Meera Nair", "Rohit Verma", "Priya Iyer",
            "Amit Shah", "Sunita Devi", "Manoj Tiwari", "Ritu Bansal"
        ]
        
        contract_types = ["Month-to-month", "One year", "Two year"]
        payment_methods = ["UPI", "Net Banking", "Credit card (automatic)", "Digital Wallet", "Electronic check"]
        
        created_count = 0
        
        # Add 1-5 predictions for each of the last 30 days
        for days_back in range(30):
            prediction_date = end_date - timedelta(days=days_back)
            
            # Random number of predictions per day (1-5)
            daily_predictions = random.randint(1, 5)
            
            for _ in range(daily_predictions):
                customer_name = random.choice(customers)
                tenure = random.randint(1, 72)
                monthly_charges = random.randint(500, 3500)
                total_charges = monthly_charges * tenure
                contract_type = random.choice(contract_types)
                payment_method = random.choice(payment_methods)
                
                # Generate realistic prediction based on tenure and contract
                if tenure < 6 and contract_type == "Month-to-month":
                    prediction = 1
                    probability = random.uniform(0.7, 0.95)
                elif tenure > 24 and contract_type in ["One year", "Two year"]:
                    prediction = 0
                    probability = random.uniform(0.05, 0.3)
                else:
                    prediction = random.choice([0, 1])
                    probability = random.uniform(0.3, 0.7)
                
                # Randomly assign to demo_user or admin
                user = random.choice([demo_user, admin_user])
                
                pred_record = Prediction(
                    user_id=user.id,
                    customer_name=customer_name,
                    tenure=tenure,
                    monthly_charges=monthly_charges,
                    total_charges=total_charges,
                    contract_type=contract_type,
                    payment_method=payment_method,
                    prediction=prediction,
                    probability=probability,
                    created_at=prediction_date
                )
                
                db.session.add(pred_record)
                created_count += 1
        
        db.session.commit()
        print(f"✅ Added {created_count} predictions across 30 days")
        
        # Verify the data
        print("\n🔍 Verifying trend data...")
        from sqlalchemy import func
        
        trends = db.session.query(
            func.date(Prediction.created_at).label('date'),
            func.count(Prediction.id).label('count')
        ).group_by(
            func.date(Prediction.created_at)
        ).order_by('date').all()
        
        print(f"📊 Total days with predictions: {len(trends)}")
        recent_trends = [t for t in trends if isinstance(t.date, str) or t.date >= (end_date - timedelta(days=30)).date()]
        print(f"📈 Days in last 30 days with predictions: {len(recent_trends)}")
        
        if recent_trends:
            print("📋 Sample trend data:")
            for trend in recent_trends[-5:]:  # Show last 5 days
                print(f"   - {trend.date}: {trend.count} predictions")

if __name__ == '__main__':
    add_trend_data()