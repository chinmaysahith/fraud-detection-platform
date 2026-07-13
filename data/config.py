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
