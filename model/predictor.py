"""
Predictor module for scoring transactions using the trained Isolation Forest model.
"""

import os
import sys
from typing import Dict, Any, List

import joblib
import numpy as np

# Add the root directory to sys.path to import data modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import config
from model.features import extract_features

class FraudPredictor:
    """
    Loads trained Isolation Forest model and scores transactions.
    """

    def __init__(self):
        """
        Loads the model from disk.
        """
        if not os.path.exists(config.MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {config.MODEL_PATH}. Train the model first.")

        self.model = joblib.load(config.MODEL_PATH)

        # Determine actual bounds from offset
        self.offset = self.model.offset_ # Offset is used to define 0 as decision boundary

        # Using min and max score to roughly scale the values correctly.
        self.min_score = -0.73
        self.max_score = -0.42

    def predict(self, txn: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predicts fraud score for a single transaction and returns an enriched dictionary.
        """
        features = extract_features(txn)

        # Isolation Forest decision_function returns > 0 for inliers (normal) and < 0 for outliers (anomalies)
        dec_func = self.model.decision_function([features])[0]

        # Convert to 0.0 - 1.0 anomaly risk score (where 1.0 is highest risk)
        fraud_score = float(np.clip(0.5 - (dec_func / 0.25), 0.0, 1.0))

        # Create a copy to enrich
        enriched_txn = txn.copy()
        enriched_txn["fraud_score"] = round(fraud_score, 2)
        enriched_txn["is_fraud_predicted"] = fraud_score >= config.FRAUD_THRESHOLD
        enriched_txn["prediction_threshold"] = config.FRAUD_THRESHOLD

        return enriched_txn

    def batch_predict(self, txns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Predicts fraud scores for a batch of transactions.
        """
        return [self.predict(txn) for txn in txns]
