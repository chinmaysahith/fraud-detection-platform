"""
Shared feature extraction logic for model training and prediction.
"""

from typing import Dict, Any, List

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

    # location_risk → risk score based on location
    location_risk_map = {
        "New York": 0.1,
        "Brooklyn": 0.1,
        "Queens": 0.1,
        "Bronx": 0.1,
        "Manhattan": 0.1,
        "Tokyo": 0.8,
        "Russia": 0.9,
        "Nigeria": 0.95,
        "North Korea": 0.99,
        "Anonymous": 0.99
    }
    location_risk = float(location_risk_map.get(txn.get("location"), 0.5))

    # merchant_risk → risk score based on merchant type
    merchant_risk_map = {
        "grocery": 0.1,
        "salon": 0.1,
        "clothing": 0.1,
        "restaurant": 0.1,
        "pharmacy": 0.1,
        "construction": 0.8,
        "weapons": 0.99,
        "unknown_store": 0.9,
        "offshore": 0.95
    }
    merchant_risk = float(merchant_risk_map.get(txn.get("merchant"), 0.5))

    # device_risk → risk score based on device
    device_risk_map = {
        "phone": 0.1,
        "laptop": 0.7,
        "unknown_device": 0.95
    }
    device_risk = float(device_risk_map.get(txn.get("device"), 0.5))

    return [amount, hour, is_weekend, location_risk, merchant_risk, device_risk]
