#!/usr/bin/env python3
"""
Debug the history page issue
"""

import sys
import os

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)

from app_flask import create_app
from models import db, User, Prediction

def debug_history():
    """Debug the history page issue"""
    app = create_app()
    
    with app.app_context():
        print("🔍 Debugging history page...")
        print("=" * 50)
        
        # Check if demo user exists
        demo_user = User.query.filter_by(username='demo_user').first()
        if demo_user:
            print(f"✅ Demo user found: {demo_user.username} (ID: {demo_user.id})")
            
            # Check predictions for demo user
            predictions = Prediction.query.filter_by(user_id=demo_user.id).all()
            print(f"📊 Total predictions for demo_user: {len(predictions)}")
            
            if predictions:
                print("📋 Sample predictions:")
                for i, pred in enumerate(predictions[:3]):
                    print(f"   {i+1}. {pred.customer_name}: {pred.prediction} ({pred.probability:.2f})")
            else:
                print("❌ No predictions found for demo_user")
        else:
            print("❌ Demo user not found")
        
        # Test the history route directly
        print("\n🧪 Testing history route directly...")
        
        with app.test_client() as client:
            # Login
            login_response = client.post('/auth/login', data={
                'username': 'demo_user',
                'password': 'user123'
            })
            
            # Get history page
            response = client.get('/history')
            print(f"📄 Direct history response: {response.status_code}")
            
            if response.status_code == 200:
                content = response.get_data(as_text=True)
                
                # Look for specific strings
                search_terms = ['Prediction History', 'predictions', 'table', 'Customer Name', 'error']
                for term in search_terms:
                    count = content.count(term)
                    if count > 0:
                        print(f"   '{term}': {count} occurrences")
                
                # Check if it's redirecting
                if 'Redirecting' in content:
                    print("⚠️  Page is redirecting")
                
                # Check for template errors
                if 'TemplateNotFound' in content:
                    print("❌ Template not found error")
                
                # Show first 200 characters
                print(f"\n📝 First 200 characters of response:")
                print(repr(content[:200]))
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.get_data(as_text=True)[:200])

if __name__ == '__main__':
    debug_history()