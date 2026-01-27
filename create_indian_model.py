#!/usr/bin/env python3
"""
Create an Indian model for the Customer Churn Prediction System
This creates a model that works with Indian rupee amounts and context
"""

import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import os

def create_indian_model():
    print("🇮🇳 Creating Indian churn prediction model...")
    
    # Create sample training data (5 features) with Indian context
    # Features: tenure, monthly_charges, total_charges, contract_encoded, payment_encoded
    np.random.seed(42)
    
    # Generate synthetic training data with Indian telecom pricing
    n_samples = 2000
    
    # Feature generation with Indian context
    tenure = np.random.randint(1, 73, n_samples)
    
    # Indian telecom monthly charges (₹500 to ₹4000)
    monthly_charges = np.random.uniform(500, 4000, n_samples)
    
    # Total charges = tenure * monthly_charges + some variation
    total_charges = tenure * monthly_charges + np.random.normal(0, 5000, n_samples)
    total_charges = np.maximum(total_charges, monthly_charges)  # Ensure total >= monthly
    
    # Contract types: 0=Month-to-month, 1=One year, 2=Two year
    contract_encoded = np.random.choice([0, 1, 2], n_samples, p=[0.5, 0.3, 0.2])
    
    # Payment methods: 0=Electronic check, 1=Mailed check, 2=Bank transfer, 3=Credit card, 4=UPI, 5=Net Banking, 6=Digital Wallet
    payment_encoded = np.random.choice([0, 1, 2, 3, 4, 5, 6], n_samples, p=[0.15, 0.05, 0.15, 0.15, 0.25, 0.15, 0.10])
    
    X = np.column_stack([tenure, monthly_charges, total_charges, contract_encoded, payment_encoded])
    
    # Create target variable (churn) with Indian telecom logic
    # Higher churn probability for:
    # - Low tenure (new customers)
    # - Very high monthly charges (price sensitive market)
    # - Month-to-month contracts
    # - Electronic check payment (less convenient)
    # - Lower churn for UPI/Digital Wallet (modern, convenient)
    
    churn_prob = np.zeros(n_samples)
    
    # Tenure factor (higher churn for new customers)
    churn_prob += np.where(tenure <= 6, 0.4, 
                  np.where(tenure <= 12, 0.3,
                  np.where(tenure <= 24, 0.2, 0.1)))
    
    # Monthly charges factor (higher churn for very high or very low charges)
    churn_prob += np.where(monthly_charges > 3000, 0.3,  # Very expensive
                  np.where(monthly_charges < 800, 0.2,   # Very cheap (might switch)
                          0.1))  # Moderate pricing
    
    # Contract factor
    contract_churn = {0: 0.4, 1: 0.2, 2: 0.1}  # Month-to-month highest churn
    for i, contract in enumerate(contract_encoded):
        churn_prob[i] += contract_churn[contract]
    
    # Payment method factor
    payment_churn = {
        0: 0.3,   # Electronic check - inconvenient
        1: 0.25,  # Mailed check - very inconvenient
        2: 0.15,  # Bank transfer - moderate
        3: 0.15,  # Credit card - moderate
        4: 0.05,  # UPI - very convenient
        5: 0.1,   # Net Banking - convenient
        6: 0.08   # Digital Wallet - convenient
    }
    for i, payment in enumerate(payment_encoded):
        churn_prob[i] += payment_churn[payment]
    
    # Add some randomness
    churn_prob += np.random.normal(0, 0.1, n_samples)
    churn_prob = np.clip(churn_prob, 0, 1)
    
    # Convert to binary labels
    y = (churn_prob > 0.5).astype(int)
    
    print(f"📊 Generated {n_samples} samples")
    print(f"📊 Churn rate: {y.mean():.2%}")
    print(f"📊 Monthly charges range: ₹{monthly_charges.min():.0f} - ₹{monthly_charges.max():.0f}")
    
    # Create and train the scaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Create and train the model
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_scaled, y)
    
    # Calculate accuracy
    accuracy = model.score(X_scaled, y)
    print(f"📊 Model accuracy: {accuracy:.2%}")
    
    # Save the model and scaler to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    
    model_path = os.path.join(backend_dir, 'churn_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"✅ Saved {model_path}")
    
    scaler_path = os.path.join(backend_dir, 'scaler.pkl')
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"✅ Saved {scaler_path}")
    
    # Test the model with Indian sample data
    print("\n🧪 Testing model with Indian data...")
    
    test_cases = [
        # [tenure, monthly_charges, total_charges, contract_encoded, payment_encoded]
        [2, 3500, 7000, 0, 0],      # High churn risk: new customer, expensive, month-to-month, electronic check
        [36, 1800, 64800, 2, 4],    # Low churn risk: long tenure, reasonable price, two year, UPI
        [6, 2500, 15000, 1, 5],     # Medium risk: short tenure, moderate price, one year, net banking
        [24, 1200, 28800, 2, 6],    # Low churn risk: good tenure, low price, two year, digital wallet
        [1, 4000, 4000, 0, 1],      # High churn risk: very new, very expensive, month-to-month, mailed check
    ]
    
    test_descriptions = [
        "High risk: New customer, expensive plan, month-to-month, electronic check",
        "Low risk: Long tenure, reasonable price, two year contract, UPI",
        "Medium risk: Short tenure, moderate price, one year, net banking", 
        "Low risk: Good tenure, low price, two year contract, digital wallet",
        "High risk: Very new, very expensive, month-to-month, mailed check"
    ]
    
    for i, (test_case, description) in enumerate(zip(test_cases, test_descriptions)):
        test_scaled = scaler.transform([test_case])
        prediction = model.predict(test_scaled)[0]
        probability = model.predict_proba(test_scaled)[0][1]
        
        print(f"\nTest case {i+1}: {description}")
        print(f"  Data: Tenure={test_case[0]}, Monthly=₹{test_case[1]}, Total=₹{test_case[2]}")
        print(f"  Prediction: {'🔴 Churn' if prediction == 1 else '🟢 No Churn'}")
        print(f"  Probability: {probability:.1%}")
    
    print("\n🎉 Indian churn prediction model created successfully!")
    print("🔄 Please restart your Flask application to load the new model.")

if __name__ == '__main__':
    create_indian_model()