"""
Shared feature extraction logic for model training and prediction.
"""

from typing import Dict, Any, List
from data import config

def extract_features(txn: Dict[str, Any]) -> List[float]:
    """
    Convert a raw transaction dictionary into numerical features for the model.
    """
    # amount → use directly as float
    amount = float(txn.get("amount", 0.0))

    # time_of_day → convert to hour number
    time_map = {
        "morning": 9,
        "afternoon": 14,
        "evening": 19,
        "midnight": 0,
        "3am": 3,
        "4am": 4
    }
    hour = float(time_map.get(txn.get("time_of_day"), 12))

    # is_weekend → 1 if weekend, 0 if weekday
    is_weekend = 1.0 if txn.get("day_of_week") in ["Saturday", "Sunday"] else 0.0

    # location_risk → risk score based on location from config
    location_risk = float(config.LOCATION_RISK_MAP.get(txn.get("location"), 0.3))

    # merchant_risk → risk score based on merchant type from config
    merchant_risk = float(config.MERCHANT_RISK_MAP.get(txn.get("merchant"), 0.3))

    # device_risk → risk score based on device from config
    device_risk = float(config.DEVICE_RISK_MAP.get(txn.get("device"), 0.2))

    return [amount, hour, is_weekend, location_risk, merchant_risk, device_risk]
