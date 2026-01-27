#!/usr/bin/env python3
"""
Main runner for Customer Churn Prediction System - Indian Edition
Organized with separate frontend and backend folders
"""

import sys
import os
import io

# Fix Unicode encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add backend to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app_flask import create_app

def main():
    """Main function to run the application"""
    print("🇮🇳 Starting Customer Churn Prediction System - Indian Edition...")
    print("📁 Frontend: templates, static files")
    print("📁 Backend: Flask app, models, routes")
    print("📊 Dashboard: http://localhost:5000")
    print("👤 Demo Admin: admin / admin123")
    print("👤 Demo User: demo_user / user123")
    print("=" * 50)
    
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()