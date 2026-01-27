#!/usr/bin/env python3
"""
Force CSS refresh by adding a timestamp
"""

import sys
import os
import time

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)

from app_flask import create_app

def force_css_refresh():
    """Add a comment to CSS to force browser refresh"""
    css_path = os.path.join(os.path.dirname(__file__), 'frontend', 'static', 'css', 'style.css')
    
    if os.path.exists(css_path):
        with open(css_path, 'r') as f:
            content = f.read()
        
        # Add a timestamp comment at the top
        timestamp = int(time.time())
        new_content = f"/* CSS Updated: {timestamp} */\n" + content
        
        with open(css_path, 'w') as f:
            f.write(new_content)
        
        print(f"✅ CSS file updated with timestamp: {timestamp}")
        print("🔄 This should force browser to reload the CSS")
    else:
        print("❌ CSS file not found")

def test_dark_mode_immediate():
    """Test dark mode with immediate feedback"""
    app = create_app()
    
    with app.test_client() as client:
        print("\n🧪 Testing dark mode fix...")
        print("=" * 50)
        
        # Login
        login_response = client.post('/auth/login', data={
            'username': 'demo_user',
            'password': 'user123',
            'submit': 'Sign In'
        }, follow_redirects=True)
        
        print(f"✅ Login: {login_response.status_code}")
        
        # Test dashboard
        dashboard = client.get('/dashboard')
        if dashboard.status_code == 200:
            content = dashboard.get_data(as_text=True)
            
            # Check if our aggressive CSS is in the HTML
            if 'body.dark-mode * { color: #ffffff !important; }' in content.replace(' ', '').replace('\n', ''):
                print("✅ Aggressive dark mode CSS found in HTML")
            else:
                print("❌ Aggressive dark mode CSS not found")
            
            # Check for inline styles
            if '<style>' in content and 'body.dark-mode' in content:
                print("✅ Inline dark mode styles found")
            else:
                print("❌ Inline dark mode styles missing")
        
        print("\n💡 Instructions:")
        print("1. Go to http://localhost:5000")
        print("2. Press Ctrl+F5 (or Cmd+Shift+R) to hard refresh")
        print("3. Login: demo_user / user123")
        print("4. Click the moon icon to toggle dark mode")
        print("5. All text should now be WHITE!")

if __name__ == '__main__':
    force_css_refresh()
    test_dark_mode_immediate()