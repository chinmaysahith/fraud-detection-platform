"""
Module for generating users and transactions.
Provides classes to simulate user profiles and generate normal and fraudulent transactions.
"""

import random
import uuid
from datetime import datetime
from typing import Dict, Any

try:
    import config
except ModuleNotFoundError:
    from data import config


class User:
    """
    Simulates a user profile with typical transaction behaviors.
    """
    def __init__(self, user_id: str):
        """
        Initializes a User with a unique ID and randomly assigned behavior ranges from config.
        """
        self.user_id = user_id
        self.home_location = random.choice(config.NORMAL_LOCATIONS)

        # Pick two amounts within the bounds and sort them to get min/max
        amt1 = random.uniform(config.NORMAL_AMOUNT_MIN, config.NORMAL_AMOUNT_MAX)
        amt2 = random.uniform(config.NORMAL_AMOUNT_MIN, config.NORMAL_AMOUNT_MAX)
        self.amount_min = min(amt1, amt2)
        self.amount_max = max(amt1, amt2)

        self.preferred_merchants = random.sample(config.NORMAL_MERCHANTS, 3)
        self.preferred_times = random.sample(config.NORMAL_TIMES, 2)
        self.device = random.choice(config.NORMAL_DEVICES)
        self.daily_frequency = random.randint(config.NORMAL_FREQUENCY_MIN, config.NORMAL_FREQUENCY_MAX)
        self.payday_multiplier = random.uniform(1.5, 2.5)

class TransactionGenerator:
    """
    Generates transactions for a given user, including normal and fraudulent ones.
    """
    def __init__(self, user: User):
        """
        Initializes the generator with a specific user profile.
        """
        self.user = user

    def _get_base_transaction(self) -> Dict[str, Any]:
        """
        Helper method to generate the base transaction skeleton.
        """
        now = datetime.now()
        return {
            "txn_id": str(uuid.uuid4()),
            "user_id": self.user.user_id,
            "amount": round(random.uniform(self.user.amount_min, self.user.amount_max), 2),
            "location": self.user.home_location,
            "merchant": random.choice(self.user.preferred_merchants),
            "device": self.user.device,
            "time_of_day": random.choice(self.user.preferred_times),
            "day_of_week": now.strftime("%A"),
            "is_fraud": False,
            "fraud_type": "none",
            "timestamp": now.isoformat()
        }

    def generate_normal(self) -> Dict[str, Any]:
        """
        Generates a normal transaction that follows the user's typical profile.
        """
        return self._get_base_transaction()

    def generate_obvious_fraud(self) -> Dict[str, Any]:
        """
        Generates an obvious fraud transaction by breaking all key properties.
        """
        txn = self._get_base_transaction()
        txn["amount"] = round(random.uniform(config.FRAUD_AMOUNT_OBVIOUS_MIN, config.FRAUD_AMOUNT_OBVIOUS_MAX), 2)
        txn["location"] = random.choice(config.FRAUD_LOCATIONS)
        txn["merchant"] = random.choice(config.FRAUD_MERCHANTS)
        txn["device"] = random.choice(config.FRAUD_DEVICES)
        txn["time_of_day"] = random.choice(config.FRAUD_TIMES)
        txn["is_fraud"] = True
        txn["fraud_type"] = "obvious"
        return txn

    def generate_subtle_fraud(self) -> Dict[str, Any]:
        """
        Generates a subtle fraud transaction by breaking 1 or 2 properties randomly.
        """
        txn = self._get_base_transaction()
        txn["is_fraud"] = True
        txn["fraud_type"] = "subtle"

        properties_to_break = random.sample(["amount", "time_of_day"], random.choice([1, 2]))

        if "amount" in properties_to_break:
            txn["amount"] = round(random.uniform(config.FRAUD_AMOUNT_SUBTLE_MIN, config.FRAUD_AMOUNT_SUBTLE_MAX), 2)
        if "time_of_day" in properties_to_break:
            txn["time_of_day"] = random.choice(config.FRAUD_TIMES)

        return txn
