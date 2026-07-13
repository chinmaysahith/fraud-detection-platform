"""
Consumer module for scoring real-time transactions from Kafka.
"""

import json
import os
import sys

from kafka import KafkaConsumer

# Add the root directory to sys.path to import data modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import config
from model.predictor import FraudPredictor
from database.db import init_db, get_connection
from database.repository import TransactionRepository

# Import drift and retrainer classes
try:
    from mlops.drift_detector import DriftDetector
    from mlops.retrainer import ModelRetrainer
except ImportError as e:
    print(f"Warning: Failed to import MLOps modules. Drift detection disabled. {e}")
    DriftDetector = None
    ModelRetrainer = None

def main():
    """
    Main loop to read from Kafka, score transactions, and print results.
    """
    try:
        predictor = FraudPredictor()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Initialize DB and Repository
    print("Initializing database...")
    try:
        init_db()
        conn = get_connection()
        repository = TransactionRepository(conn)
    except Exception as e:
        print(f"Database connection error on startup: {e}")
        repository = None
        conn = None

    # Initialize MLOps components
    drift_detector = None
    retrainer = None
    if DriftDetector and ModelRetrainer:
        try:
            print("Initializing Drift Detector...")
            drift_detector = DriftDetector()
            retrainer = ModelRetrainer()
        except Exception as e:
            print(f"Error initializing MLOps components: {e}")

    print(f"Connecting to Kafka broker at {config.KAFKA_BROKER}...")

    try:
        consumer = KafkaConsumer(
            config.KAFKA_TOPIC,
            bootstrap_servers=[config.KAFKA_BROKER],
            group_id=config.KAFKA_GROUP_ID,
            auto_offset_reset=config.KAFKA_AUTO_OFFSET_RESET,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        print(f"Listening to topic '{config.KAFKA_TOPIC}'...")

        transaction_buffer = []
        transaction_count = 0

        for message in consumer:
            txn = message.value

            # Buffer for drift detection
            transaction_buffer.append(txn)
            transaction_count += 1

            # Predict
            scored_txn = predictor.predict(txn)

            score = scored_txn["fraud_score"]
            txn_id = scored_txn["txn_id"][:6]
            user = scored_txn["user_id"]
            amount = float(scored_txn["amount"])

            # Label logic
            if score < 0.5:
                label = "[SAFE  ✅]"
            elif score < 0.8:
                label = "[REVIEW⚠️]"
            else:
                label = "[FRAUD 🚨]"

            db_status_str = "✅"
            if repository:
                try:
                    # Save transaction to DB
                    save_txn_success = repository.save_transaction(scored_txn)

                    # Save fraud alert if score >= 0.5
                    save_alert_success = True
                    if score >= 0.5:
                        save_alert_success = repository.save_fraud_alert(scored_txn)

                    if not save_txn_success or (score >= 0.5 and not save_alert_success):
                        db_status_str = "❌"
                except Exception as e:
                    print(f"Error saving to DB: {e}")
                    db_status_str = "❌"
            else:
                db_status_str = "❌"

            print(f"{label} txn_id: {txn_id} | user: {user} | amount: ${amount:.2f} | score: {score:.2f} | db: {db_status_str}")

            # Drift Check
            if transaction_count % config.DRIFT_CHECK_INTERVAL == 0:
                print(f"\n🔍 Drift check at {transaction_count} transactions...")
                if drift_detector and retrainer:
                    try:
                        drift_result = drift_detector.check_drift(transaction_buffer)
                        score = drift_result['drift_score']

                        if drift_detector.should_retrain(drift_result):
                            print(f"📊 Drift score: {score:.2f} → DRIFT DETECTED 🚨 Retraining...")
                            retrain_result = retrainer.retrain()
                            retrainer.log_retrain_event(drift_result, retrain_result)

                            # Reload model
                            try:
                                predictor = FraudPredictor()
                                print(f"✅ Model retrained and reloaded successfully ({retrain_result.get('model_version', 'v_new')})")
                            except Exception as e:
                                print(f"Error reloading model: {e}")
                        else:
                            print(f"📊 Drift score: {score:.2f} → No retraining needed ✅")

                    except Exception as e:
                        print(f"Error during drift check: {e}")
                else:
                    print("Drift detection components not loaded. Skipping drift check.")

                # Clear buffer
                transaction_buffer = []
                print() # Empty line for readability

    except KeyboardInterrupt:
        print("\nStopping inference consumer...")
    except Exception as e:
        print(f"\nKafka connection error: {e}")
    finally:
        if 'conn' in locals() and conn:
            from database.db import close_connection
            close_connection(conn)

if __name__ == "__main__":
    main()
