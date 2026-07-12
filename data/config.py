"""
Configuration file for data generation parameters.
Defines constants for users, transactions, normal behavior, and fraud behavior.
"""

# Number of fake users to simulate
NUM_USERS = 100

# Transactions per second
TRANSACTIONS_PER_SECOND = 10

# Fraud probabilities
OBVIOUS_FRAUD_PROBABILITY = 0.04   # 4%
SUBTLE_FRAUD_PROBABILITY = 0.01    # 1%
NORMAL_PROBABILITY = 0.95          # 95%

# Normal user behavior ranges
NORMAL_AMOUNT_MIN = 100
NORMAL_AMOUNT_MAX = 1000
NORMAL_LOCATIONS = ["New York", "Brooklyn", "Queens", "Bronx", "Manhattan"]
NORMAL_MERCHANTS = ["grocery", "salon", "clothing", "restaurant", "pharmacy"]
NORMAL_DEVICES = ["phone"]
NORMAL_TIMES = ["morning", "afternoon", "evening"]
NORMAL_FREQUENCY_MIN = 5
NORMAL_FREQUENCY_MAX = 10

# Fraud behavior values
FRAUD_AMOUNT_OBVIOUS_MIN = 8000
FRAUD_AMOUNT_OBVIOUS_MAX = 15000
FRAUD_AMOUNT_SUBTLE_MIN = 5000
FRAUD_AMOUNT_SUBTLE_MAX = 8000
FRAUD_LOCATIONS = ["Tokyo", "Russia", "Nigeria", "North Korea", "Anonymous"]
FRAUD_MERCHANTS = ["construction", "weapons", "unknown_store", "offshore"]
FRAUD_DEVICES = ["laptop", "unknown_device"]
FRAUD_TIMES = ["midnight", "3am", "4am"]
