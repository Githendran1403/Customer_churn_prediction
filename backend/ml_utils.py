import pickle
import numpy as np
from config import Config

class ChurnPredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_models()
    
    def load_models(self):
        try:
            with open(Config.MODEL_PATH, 'rb') as f:
                self.model = pickle.load(f)
            with open(Config.SCALER_PATH, 'rb') as f:
                self.scaler = pickle.load(f)
        except FileNotFoundError as e:
            print(f"Model files not found: {e}")
            raise
    
    def encode_features(self, contract_type, payment_method):
        """Encode categorical features for Indian context"""
        contract_map = {
            "Month-to-month": 0,
            "One year": 1,
            "Two year": 2
        }
        
        payment_map = {
            "Electronic check": 0,
            "Mailed check": 1,
            "Bank transfer (automatic)": 2,
            "Credit card (automatic)": 3,
            "UPI": 4,
            "Net Banking": 5,
            "Digital Wallet": 6
        }
        
        return contract_map.get(contract_type, 0), payment_map.get(payment_method, 0)
    
    def predict(self, tenure, monthly_charges, total_charges, contract_type, payment_method):
        """Make prediction for customer churn"""
        if not self.model or not self.scaler:
            raise ValueError("Models not loaded properly")
        
        # Encode categorical features
        contract_encoded, payment_encoded = self.encode_features(contract_type, payment_method)
        
        # Prepare input data
        input_data = np.array([[
            tenure,
            monthly_charges,
            total_charges,
            contract_encoded,
            payment_encoded
        ]])
        
        # Scale the input
        input_scaled = self.scaler.transform(input_data)
        
        # Make prediction
        prediction = self.model.predict(input_scaled)[0]
        probability = self.model.predict_proba(input_scaled)[0]
        
        # Return prediction and probability of churn
        churn_probability = probability[1] if len(probability) > 1 else probability[0]
        
        return int(prediction), float(churn_probability)

# Global predictor instance
predictor = ChurnPredictor()