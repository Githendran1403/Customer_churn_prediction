#!/usr/bin/env python3
"""
Customer Churn Prediction System
Main application runner
"""

from app_flask import create_app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Starting Customer Churn Prediction System...")
    print("📊 Dashboard: http://localhost:5000")
    print("👤 Demo Admin: admin / admin123")
    print("👤 Demo User: user / user123")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)