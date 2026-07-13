"""
Module for detecting data drift using Evidently AI.
"""

import os
import sys
import pickle
from datetime import datetime
from typing import List, Dict, Any

import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

# Add the root directory to sys.path to import data modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import config
from data.generator import User, TransactionGenerator
from model.features import extract_features

class DriftDetector:
    """
    Detects data drift using Evidently AI.
    """

    def __init__(self):
        """
        Initializes the DriftDetector. Loads reference data if it exists,
        otherwise generates fresh reference data and saves it.
        """
        self.reference_path = config.REFERENCE_DATA_PATH
        if os.path.exists(self.reference_path):
            with open(self.reference_path, 'rb') as f:
                self.reference_df = pickle.load(f)
        else:
            self.save_reference_data()

    def save_reference_data(self) -> None:
        """
        Generates 1000 normal transactions, extracts features, and saves
        them as a DataFrame to the reference data path using pickle.
        """
        features_list = []
        for i in range(1000):
            user = User(f"user_ref_{i}")
            generator = TransactionGenerator(user)
            txn = generator.generate_normal()
            features = extract_features(txn)
            features_list.append(features)

        self.reference_df = pd.DataFrame(features_list, columns=config.FEATURE_COLUMNS)

        os.makedirs(os.path.dirname(self.reference_path), exist_ok=True)
        with open(self.reference_path, 'wb') as f:
            pickle.dump(self.reference_df, f)

    def check_drift(self, current_transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Takes a list of recent transaction dictionaries, extracts features,
        and uses Evidently to compare against reference data.

        Args:
            current_transactions: A list of dictionaries representing transactions.

        Returns:
            A dictionary containing drift results.
        """
        features_list = []
        for txn in current_transactions:
            features = extract_features(txn)
            features_list.append(features)

        current_df = pd.DataFrame(features_list, columns=config.FEATURE_COLUMNS)

        report = Report(metrics=[DataDriftPreset()])
        report.run(
            reference_data=self.reference_df,
            current_data=current_df
        )

        result = report.as_dict()
        drift_score = result["metrics"][0]["result"]["drift_share"]
        drifted_features = [
            feature for feature, details in result["metrics"][0]["result"]["drift_by_columns"].items()
            if details["drift_detected"]
        ]

        drift_detected = drift_score > config.DRIFT_THRESHOLD

        return {
            "drift_detected": drift_detected,
            "drift_score": drift_score,
            "drifted_features": drifted_features,
            "timestamp": datetime.now().isoformat()
        }

    def should_retrain(self, drift_result: Dict[str, Any]) -> bool:
        """
        Determines if retraining is necessary based on the drift score.

        Args:
            drift_result: The dictionary returned by `check_drift`.

        Returns:
            True if the drift score is greater than DRIFT_THRESHOLD, False otherwise.
        """
        return drift_result.get("drift_score", 0.0) > config.DRIFT_THRESHOLD