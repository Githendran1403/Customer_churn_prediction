#!/usr/bin/env python3
"""
Check database data for debugging prediction trends
"""

import sys
import os
from datetime import datetime, timedelta

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)

from app_flask import create_app
from models import db, User, Prediction
from sqlalchemy import func

def check_data():
    """Check what data exists in the database"""
    app = create_app()
    
    with app.app_context():
        print("🔍 Checking database data...")
        print("=" * 50)
        
        # Check users
        users = User.query.all()
        print(f"👥 Total users: {len(users)}")
        for user in users:
            print(f"   - {user.username} ({user.role})")
        
        # Check predictions
        predictions = Prediction.query.all()
        print(f"\n📊 Total predictions: {len(predictions)}")
        
        if predictions:
            print("\n📋 Prediction details:")
            for pred in predictions[:5]:  # Show first 5
                print(f"   - {pred.customer_name}: {pred.prediction} ({pred.probability:.2f}) - {pred.created_at}")
            
            if len(predictions) > 5:
                print(f"   ... and {len(predictions) - 5} more")
        
        # Check prediction trends data (same query as admin route)
        print("\n📈 Prediction trends data:")
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        trends = db.session.query(
            func.date(Prediction.created_at).label('date'),
            func.count(Prediction.id).label('count')
        ).filter(
            Prediction.created_at >= start_date
        ).group_by(
            func.date(Prediction.created_at)
        ).order_by('date').all()
        
        print(f"   Found {len(trends)} days with predictions:")
        for trend in trends:
            print(f"   - {trend.date}: {trend.count} predictions")
        
        if not trends:
            print("   ❌ No prediction trends data found!")
            print("   🔍 Checking all predictions by date:")
            all_predictions = db.session.query(
                func.date(Prediction.created_at).label('date'),
                func.count(Prediction.id).label('count')
            ).group_by(
                func.date(Prediction.created_at)
            ).order_by('date').all()
            
            for pred in all_predictions:
                print(f"   - {pred.date}: {pred.count} predictions")

if __name__ == '__main__':
    check_data()