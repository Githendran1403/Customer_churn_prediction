# Customer Churn Prediction System - Frontend

A modern, responsive frontend for the Customer Churn Prediction System, specially designed for Indian businesses with local context and currency (₹).

## 🇮🇳 Made for India

- **Indian Currency**: All amounts displayed in Indian Rupees (₹)
- **Local Business Context**: Examples from Indian telecom, banking, and e-commerce
- **Indian Payment Methods**: UPI, Net Banking, Digital Wallets
- **Professional UI**: Clean, modern design optimized for Indian users
- **Mobile Responsive**: Works perfectly on all devices popular in India

## 📁 Frontend Structure

```
frontend/
├── 📁 templates/                  # HTML Templates (Jinja2)
│   ├── base.html                 # Base template with navigation
│   ├── index.html                # Landing page
│   ├── dashboard.html            # User dashboard with charts
│   ├── predict.html              # Prediction form
│   ├── history.html              # Prediction history
│   ├── settings.html             # User settings
│   ├── 📁 auth/                  # Authentication templates
│   │   ├── login.html
│   │   └── register.html
│   └── 📁 admin/                 # Admin templates
│       └── dashboard.html
├── 📁 static/                    # Static Assets
│   ├── 📁 css/
│   │   └── style.css             # Custom styles with Indian theme
│   └── 📁 js/
│       └── main.js               # JavaScript functionality
├── package.json                  # Frontend dependencies
├── README.md                     # This file
└── .gitignore                    # Git ignore rules
```

## 🎨 Design Features

### **Indian Theme**
- **Color Scheme**: Professional blue and purple gradients
- **Currency Display**: ₹ symbol throughout the interface
- **Indian Context**: Business examples from Jio, Airtel, SBI, HDFC
- **Payment Methods**: UPI, Net Banking, Digital Wallets prominently featured

### **Modern UI/UX**
- **Bootstrap 5**: Responsive CSS framework
- **Font Awesome**: Professional iconography
- **Google Fonts**: Inter font family for readability
- **Custom CSS Variables**: Consistent theming
- **Mobile-First**: Optimized for mobile devices

### **Interactive Elements**
- **Plotly.js Charts**: Beautiful, interactive data visualizations
- **Real-time Updates**: Dynamic content loading
- **Smooth Animations**: CSS transitions and hover effects
- **Loading States**: User feedback during operations
- **Flash Messages**: Success, error, and info notifications

## 🚀 Key Pages

### **1. Landing Page (index.html)**
- Hero section with Indian business focus
- Feature cards highlighting AI predictions
- Statistics display for logged-in users
- How it works section with Indian examples

### **2. Dashboard (dashboard.html)**
- Interactive charts with ₹ amounts
- Key metrics and statistics
- Recent predictions overview
- Model performance indicators

### **3. Prediction Form (predict.html)**
- Clean, intuitive form design
- Indian payment method options
- Real-time validation
- Sample data helpers with Indian examples

### **4. History (history.html)**
- Paginated prediction history
- Advanced filtering options
- Export to CSV functionality
- Detailed prediction modals

### **5. Admin Dashboard (admin/dashboard.html)**
- System-wide statistics
- User management interface
- Model performance metrics
- Prediction trends analysis

## 💰 Indian Business Context

### **Sample Customer Data**
```
High Risk Customer:
- Name: Rajesh Kumar
- Monthly Charges: ₹2,500
- Payment: Electronic check
- Contract: Month-to-month

Low Risk Customer:
- Name: Priya Sharma
- Monthly Charges: ₹1,950
- Payment: UPI
- Contract: Two year
```

### **Payment Methods Supported**
- **UPI** (Unified Payments Interface)
- **Net Banking**
- **Digital Wallet** (Paytm/PhonePe/GPay)
- **Credit Card (automatic)**
- **Electronic check**
- **Mailed check**

### **Industry Examples**
- **Telecom**: Jio, Airtel, Vi (₹199-₹999 plans)
- **Banking**: SBI, HDFC, ICICI (₹0-₹1000 fees)
- **E-commerce**: Flipkart, Amazon India (₹99-₹1499 memberships)

## 🛠️ Technologies Used

### **Frontend Framework**
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with flexbox/grid
- **JavaScript (ES6+)**: Interactive functionality
- **Bootstrap 5**: Responsive components

### **Libraries & Tools**
- **Plotly.js**: Interactive charts and graphs
- **Font Awesome**: Icon library
- **Google Fonts**: Typography (Inter font family)
- **jQuery**: DOM manipulation (minimal usage)

### **Template Engine**
- **Jinja2**: Server-side templating (Flask integration)
- **Template Inheritance**: DRY principle with base templates
- **Context Variables**: Dynamic content rendering

## 📱 Responsive Design

### **Mobile Optimization**
- **Touch-friendly**: Large buttons and touch targets
- **Readable Text**: Optimized font sizes for mobile
- **Collapsible Navigation**: Mobile-friendly menu
- **Fast Loading**: Optimized assets and minimal dependencies

### **Device Support**
- **📱 Mobile**: Android/iOS phones (320px+)
- **📱 Tablet**: iPad, Android tablets (768px+)
- **💻 Desktop**: All screen sizes (1024px+)
- **🖥️ Large Screens**: 4K and ultrawide support

## 🎯 Indian User Experience

### **Localized Content**
- **Currency**: All amounts in ₹ (Indian Rupees)
- **Business Names**: Indian customer names (Rajesh, Priya, Amit)
- **Company References**: Jio, Airtel, SBI, HDFC, Flipkart
- **Payment Context**: UPI and Net Banking prominently featured

### **Cultural Considerations**
- **Professional Design**: Suitable for corporate environments
- **Clear Hierarchy**: Easy navigation for all user levels
- **Familiar Patterns**: Standard web conventions
- **Accessibility**: WCAG compliance considerations

## 🔧 Customization

### **Theming**
The CSS uses custom properties for easy theming:

```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --success-color: #10b981;
    --danger-color: #ef4444;
    --rupee-color: #2d5a27;
}
```

### **Indian Customizations**
- **Rupee Symbol**: Proper ₹ formatting
- **Number Format**: Indian numbering (1,00,000)
- **Date Format**: DD/MM/YYYY (Indian standard)
- **Business Context**: Industry-specific examples

## 🚀 Integration with Backend

### **API Endpoints**
The frontend expects these backend endpoints:

- `GET /` - Landing page
- `GET /dashboard` - User dashboard
- `POST /predict` - Make predictions
- `GET /history` - Prediction history
- `GET /api/prediction-stats` - Statistics API
- `GET /api/monthly-trend` - Trend data API

### **Data Format**
Expected JSON format for API responses:

```json
{
  "prediction": 1,
  "probability": 0.87,
  "customer_name": "Rajesh Kumar",
  "monthly_charges": 2500,
  "currency": "₹"
}
```

## 📦 Dependencies

### **CDN Libraries**
- Bootstrap 5.3.0
- Font Awesome 6.4.0
- Plotly.js (latest)
- Google Fonts (Inter)

### **Local Assets**
- Custom CSS (style.css)
- Custom JavaScript (main.js)

## 🔄 Future Enhancements

### **Planned Features**
- **Progressive Web App** (PWA) support
- **Offline Functionality** for basic features
- **Push Notifications** for prediction alerts
- **Voice Input** for Hindi commands
- **Dark Mode** theme option
- **Multi-language** support (Hindi, Tamil, Bengali)

### **Technical Improvements**
- **React/Vue Migration** for SPA experience
- **TypeScript** for better development
- **Webpack/Vite** for build optimization
- **Service Workers** for caching
- **WebSocket** for real-time updates

## 📄 License

This frontend is part of the Customer Churn Prediction System and is available under the MIT License.

---

**Built with ❤️ for Indian Businesses**
**Modern Frontend Architecture for Scalability**