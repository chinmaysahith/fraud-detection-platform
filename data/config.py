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
NORMAL_AMOUNT_MIN = 1
NORMAL_AMOUNT_MAX = 1000
NORMAL_LOCATIONS = ["USA", "United States", "UK", "United Kingdom", "Germany", "Japan", "UAE", "New York", "Brooklyn", "Queens", "Manhattan"]
NORMAL_MERCHANTS = ["grocery", "salon", "clothing", "restaurant", "pharmacy", "electronics"]
NORMAL_DEVICES = ["phone", "mobile"]
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

# Kafka Configuration
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "txn-stream"
KAFKA_GROUP_ID = "fraud-detector-group"
KAFKA_AUTO_OFFSET_RESET = "earliest"

# Model Configuration
FRAUD_THRESHOLD = 0.8
TRAINING_SAMPLES = 10000
MODEL_PATH = "model/isolation_forest.pkl"
CONTAMINATION = 0.05  # expected 5% fraud in real data

# Feature columns used for training and inference
FEATURE_COLUMNS = ["amount", "hour", "is_weekend", "location_risk", "merchant_risk", "device_risk"]

# PostgreSQL Configuration
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DB = "fraud_detection"
POSTGRES_USER = "fraud_user"
POSTGRES_PASSWORD = "fraud_pass"
POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# MLflow Configuration
MLFLOW_TRACKING_URI = "http://localhost:5000"
MLFLOW_EXPERIMENT_NAME = "fraud-detection"
MODEL_NAME = "isolation-forest-fraud"

# Drift Detection Configuration
DRIFT_CHECK_INTERVAL = 500      # check every 500 transactions
DRIFT_THRESHOLD = 0.3           # retrain if drift score > 0.3
REFERENCE_DATA_PATH = "mlops/reference_data.pkl"

# Retraining Configuration
RETRAIN_SAMPLES = 10000

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
API_KEY = "fraud-api-key-x7k9m2p4"
API_KEY_NAME = "X-API-Key"
API_TITLE = "Fraud Detection API"
API_DESCRIPTION = "Real-time fraud detection platform API"
API_VERSION = "1.0.0"

# Feature Risk Maps
LOCATION_RISK_MAP = {
    "USA": 0.1,
    "United States": 0.1,
    "UK": 0.1,
    "United Kingdom": 0.1,
    "Germany": 0.1,
    "Japan": 0.1,
    "UAE": 0.2,
    "New York": 0.1,
    "Brooklyn": 0.1,
    "Queens": 0.1,
    "Bronx": 0.1,
    "Manhattan": 0.1,
    "Brazil": 0.5,
    "Tokyo": 0.3,
    "Russia": 0.9,
    "Nigeria": 0.95,
    "North Korea": 0.99,
    "Anonymous": 0.99
}

MERCHANT_RISK_MAP = {
    "grocery": 0.1,
    "salon": 0.1,
    "clothing": 0.1,
    "restaurant": 0.1,
    "pharmacy": 0.1,
    "electronics": 0.2,
    "luxury_watch": 0.7,
    "casino": 0.85,
    "crypto_exchange": 0.9,
    "weapons": 0.99,
    "construction": 0.6,
    "unknown_store": 0.9,
    "offshore": 0.95
}

DEVICE_RISK_MAP = {
    "phone": 0.1,
    "mobile": 0.1,
    "tablet": 0.2,
    "POS_terminal": 0.2,
    "laptop": 0.3,
    "unknown_device": 0.95
}
