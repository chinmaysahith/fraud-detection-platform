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

def main():
    """
    Main loop to read from Kafka, score transactions, and print results.
    """
    try:
        predictor = FraudPredictor()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

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

            print(f"{label} txn_id: {txn_id} | user: {user} | amount: ${amount:.2f} | score: {score:.2f}")

    except KeyboardInterrupt:
        print("\nStopping inference consumer...")
    except Exception as e:
        print(f"\nKafka connection error: {e}")

if __name__ == "__main__":
    main()
