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

        # Isolation Forest returns negative scores
        # Convert to 0.0-1.0 probability:
        raw_score = self.model.score_samples([features])[0]

        # raw_score is negative: more negative = more anomalous
        # normalize to 0-1 where 1 = most anomalous
        fraud_score = 1 - (raw_score - self.min_score) / (self.max_score - self.min_score)

        # Use clip to ensure range stays 0.0-1.0
        fraud_score = float(np.clip(fraud_score, 0.0, 1.0))

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
