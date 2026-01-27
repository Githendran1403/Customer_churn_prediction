#!/usr/bin/env python3
"""
Create a demo model for the Customer Churn Prediction System
This creates a simple model that works with our 5 features
"""

import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

def create_demo_model():
    print("🔄 Creating demo model...")
    
    # Create sample training data (5 features)
    # Features: tenure, monthly_charges, total_charges, contract_encoded, payment_encoded
    np.random.seed(42)
    
    # Generate synthetic training data
    n_samples = 1000
    
    # Feature generation
    tenure = np.random.randint(1, 73, n_samples)
    monthly_charges = np.random.uniform(20, 120, n_samples)
    total_charges = tenure * monthly_charges + np.random.normal(0, 100, n_samples)
    contract_encoded = np.random.randint(0, 3, n_samples)  # 0, 1, 2
    payment_encoded = np.random.randint(0, 4, n_samples)   # 0, 1, 2, 3
    
    X = np.column_stack([tenure, monthly_charges, total_charges, contract_encoded, payment_encoded])
    
    # Create target variable (churn) with some logic
    # Higher churn probability for:
    # - Low tenure
    # - High monthly charges
    # - Month-to-month contracts (0)
    # - Electronic check payment (0)
    
    churn_prob = (
        (72 - tenure) / 72 * 0.3 +  # Lower tenure = higher churn
        (monthly_charges - 20) / 100 * 0.2 +  # Higher charges = higher churn
        (contract_encoded == 0) * 0.3 +  # Month-to-month = higher churn
        (payment_encoded == 0) * 0.2  # Electronic check = higher churn
    )
    
    # Add some randomness
    churn_prob += np.random.normal(0, 0.1, n_samples)
    churn_prob = np.clip(churn_prob, 0, 1)
    
    # Convert to binary labels
    y = (churn_prob > 0.5).astype(int)
    
    print(f"📊 Generated {n_samples} samples")
    print(f"📊 Churn rate: {y.mean():.2%}")
    
    # Create and train the scaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Create and train the model
    model = LogisticRegression(random_state=42)
    model.fit(X_scaled, y)
    
    # Calculate accuracy
    accuracy = model.score(X_scaled, y)
    print(f"📊 Model accuracy: {accuracy:.2%}")
    
    # Save the model and scaler
    with open('churn_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("✅ Saved churn_model.pkl")
    
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    print("✅ Saved scaler.pkl")
    
    # Test the model with sample data
    print("\n🧪 Testing model...")
    
    test_cases = [
        [2, 85, 170, 0, 0],    # High churn risk
        [36, 65, 2340, 2, 3],  # Low churn risk
    ]
    
    for i, test_case in enumerate(test_cases):
        test_scaled = scaler.transform([test_case])
        prediction = model.predict(test_scaled)[0]
        probability = model.predict_proba(test_scaled)[0][1]
        
        print(f"Test case {i+1}: {test_case}")
        print(f"  Prediction: {'Churn' if prediction == 1 else 'No Churn'}")
        print(f"  Probability: {probability:.2%}")
    
    print("\n🎉 Demo model created successfully!")

if __name__ == '__main__':
    create_demo_model()