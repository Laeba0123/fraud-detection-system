import joblib
import numpy as np
import os
from app.config import settings

# Path to your new final artifact
MODEL_PATH = os.path.join("models", "final_model.pkl")

class FraudModel:
    def __init__(self):
        self.pipeline = None

    def load_model(self):
        try:
            # This now loads the Scaler + Random Forest together
            self.pipeline = joblib.load(MODEL_PATH)
            print("[INFO] Fraud Pipeline loaded successfully")
        except Exception as e:
            raise RuntimeError(f"Error loading pipeline: {e}")

    def validate_input(self, data):
        if not isinstance(data, list) or len(data) != 30:
            raise ValueError(f"Expected 30 features in a list, got {len(data)}")

    def predict(self, data: list):
        try:
            self.validate_input(data)

            # Convert to numpy array
            data_array = np.array(data).reshape(1, -1)

            # --- NO MANUAL SCALING NEEDED ---
            # The pipeline automatically scales the data using the embedded scaler
            # before passing it to the Random Forest.
            prob = float(self.pipeline.predict_proba(data_array)[0][1])
            
            prediction = "FRAUD" if prob >= settings.MODEL_THRESHOLD else "NORMAL"
            confidence = self.get_confidence(prob)

            return {
                "prediction": prediction,
                "probability": round(prob, 4),
                "confidence_level": confidence
            }

        except Exception as e:
            raise RuntimeError(f"Inference error: {e}")

    def get_confidence(self, prob):
        if prob >= 0.9 or prob <= 0.1: return "HIGH"
        elif prob >= 0.7 or prob <= 0.3: return "MEDIUM"
        else: return "LOW"

fraud_model = FraudModel()