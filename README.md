# 📊 ChurnPredict India - AI-Powered Customer Retention Analytics

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

> **🚀 Unique Feature**: First customer churn prediction system with professional email reporting capabilities for Indian businesses!

## ✨ Features

### 🎯 **Core Functionality**
- **AI-Powered Predictions**: Advanced machine learning model for accurate churn prediction
- **Indian Business Context**: Rupee (₹) currency formatting and Indian telecom industry insights
- **Single & Bulk Predictions**: Handle individual customers or process CSV files with hundreds of records
- **Risk Scoring**: 0-100 risk scores with color-coded visualization
- **Historical Analytics**: Track prediction trends and model performance

### 📧 **Unique Email Reporting** (Our Competitive Advantage)
- **Professional HTML Emails**: Beautiful, responsive email templates with ChurnPredict India branding
- **Stakeholder Communication**: Share prediction reports with managers and decision-makers
- **Bulk Reports**: Comprehensive email reports for multiple customer predictions
- **Actionable Insights**: Risk-based recommendations and business strategies
- **Audit Trail**: Email records for compliance and documentation

### 🎨 **User Experience**
- **Dark Mode Support**: Complete dark theme with proper text visibility
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Admin Dashboard**: System analytics, user management, and model metrics
- **User Authentication**: Secure login system with role-based access
- **Interactive Charts**: Plotly-powered visualizations with dark mode support

### 🔧 **Technical Excellence**
- **Production Ready**: Complete error handling, logging, and security
- **Scalable Architecture**: Modular Flask application with blueprints
- **Database Management**: SQLAlchemy ORM with SQLite/PostgreSQL support
- **Email Integration**: Flask-Mail with SMTP configuration
- **Modern Frontend**: Bootstrap 5 with custom CSS and JavaScript

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Githendran1403/Customer_churn_prediction.git
   cd Customer_churn_prediction
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure email (optional)**
   ```bash
   # For Gmail
   set MAIL_USERNAME=your-email@gmail.com
   set MAIL_PASSWORD=your-app-password
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Access the application**
   - Open: http://localhost:5000
   - Login: `admin` / `admin123` or `demo_user` / `user123`

## 📧 Email Feature Setup

### Gmail Configuration
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account → Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Set environment variables:
   ```bash
   set MAIL_USERNAME=your-email@gmail.com
   set MAIL_PASSWORD=your-16-digit-app-password
   set MAIL_SERVER=smtp.gmail.com
   set MAIL_PORT=587
   ```

### Using Email Features
1. Make a prediction (single or bulk)
2. Scroll down to find "Share Prediction Report" section
3. Enter recipient email and your name
4. Click "Send Email Report"
5. Professional report will be sent instantly!

## 🎯 Usage Guide

### Single Prediction
1. Navigate to **Predict** page
2. Fill customer details:
   - Customer Name: `Rajesh Kumar`
   - Tenure: `12` months
   - Monthly Charges: `₹2,500`
   - Total Charges: `₹30,000`
   - Contract Type: `Two year`
   - Payment Method: `Credit card (automatic)`
3. Click **Predict** to get results
4. Use email sharing to send reports to stakeholders

### Bulk Predictions
1. Navigate to **Bulk Predict** page
2. Download sample CSV template
3. Upload your customer data CSV
4. Review processing results
5. Send bulk email reports to management

### Admin Features
- **User Management**: Create, activate/deactivate users
- **System Analytics**: Prediction trends and performance metrics
- **Model Metrics**: Accuracy, precision, recall, F1-score tracking
- **Bulk Operations**: Manage large-scale predictions

## 🏗️ Architecture

```
Customer_churn_project/
├── backend/
│   ├── app_flask.py          # Flask application factory
│   ├── config.py             # Configuration settings
│   ├── email_utils.py        # Email functionality
│   ├── models.py             # Database models
│   ├── ml_utils.py           # Machine learning utilities
│   ├── forms.py              # WTForms definitions
│   └── routes/               # Application routes
│       ├── auth.py           # Authentication routes
│       ├── main.py           # Main application routes
│       ├── admin.py          # Admin panel routes
│       └── api.py            # API endpoints
├── frontend/
│   ├── templates/            # Jinja2 templates
│   ├── static/
│   │   ├── css/style.css     # Custom styles with dark mode
│   │   └── js/main.js        # JavaScript functionality
├── requirements.txt          # Python dependencies
└── run.py                   # Application entry point
```

## 🎨 Screenshots

### Dashboard
![Dashboard](https://via.placeholder.com/800x400/2563eb/ffffff?text=Dashboard+with+Analytics)

### Prediction Interface
![Prediction](https://via.placeholder.com/800x400/059669/ffffff?text=Prediction+Interface)

### Email Report
![Email](https://via.placeholder.com/800x400/dc2626/ffffff?text=Professional+Email+Report)

## 🔧 Technical Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login, Flask-Mail
- **Frontend**: Bootstrap 5, Custom CSS, JavaScript
- **Machine Learning**: scikit-learn, pandas, numpy
- **Database**: SQLite (development), PostgreSQL (production)
- **Visualization**: Plotly.js
- **Email**: Flask-Mail with SMTP support

## 🌟 Unique Selling Points

1. **📧 Email Reporting**: First churn prediction tool with professional email capabilities
2. **🇮🇳 Indian Context**: Rupee formatting and Indian telecom industry insights
3. **🎨 Dark Mode**: Complete dark theme with proper accessibility
4. **📊 Bulk Processing**: Handle hundreds of customers with comprehensive reports
5. **👥 Stakeholder Communication**: Professional reports for business decision-makers
6. **🔒 Production Ready**: Complete authentication, security, and error handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Githendran**
- GitHub: [@Githendran1403](https://github.com/Githendran1403)
- Email: githendran14232005@gmail.com

## 🙏 Acknowledgments

- Built with Flask and modern web technologies
- Inspired by the need for better customer retention analytics in Indian businesses
- Special focus on professional communication and stakeholder reporting

---

⭐ **Star this repository if you find it helpful!**

🚀 **Ready to predict customer churn with professional email reporting? Get started now!**