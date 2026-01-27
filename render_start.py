#!/usr/bin/env python3
"""
Production entry point for Render deployment
"""
import os
import sys

# Add backend to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app_flask import create_app

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 Starting production server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)