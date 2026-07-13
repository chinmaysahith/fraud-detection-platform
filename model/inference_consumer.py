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

        for message in consumer:
            txn = message.value

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
