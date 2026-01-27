#!/usr/bin/env python3
"""
Setup script for Customer Churn Prediction System
This script sets up the complete application with demo data
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Customer Churn Prediction System Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not run_command("pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF WTForms Werkzeug pandas numpy plotly python-dotenv bcrypt email_validator", 
                      "Installing dependencies"):
        print("❌ Failed to install dependencies. Please install manually:")
        print("pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF WTForms Werkzeug pandas numpy plotly python-dotenv bcrypt email_validator")
        return False
    
    # Create demo model if needed
    if not os.path.exists('churn_model.pkl') or not os.path.exists('scaler.pkl'):
        if not run_command("python create_demo_model.py", "Creating demo ML model"):
            print("❌ Failed to create demo model")
            return False
    else:
        print("✅ ML model files already exist")
    
    # Initialize demo data
    if not run_command("python init_demo_data.py", "Creating demo data"):
        print("⚠️  Demo data creation failed, but the app should still work")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run: python run.py")
    print("2. Open: http://localhost:5000")
    print("3. Login with:")
    print("   👤 Admin: admin / admin123")
    print("   👤 User: user / user123")
    print("\n🌟 Features available:")
    print("• Landing page with feature overview")
    print("• User authentication and registration")
    print("• AI-powered churn predictions")
    print("• Interactive dashboard with charts")
    print("• Prediction history with filtering")
    print("• Admin panel for user management")
    print("• Data export functionality")
    print("• Responsive mobile-friendly design")
    
    return True

if __name__ == '__main__':
    success = main()
    if not success:
        sys.exit(1)