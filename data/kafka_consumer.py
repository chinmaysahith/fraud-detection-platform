"""
Test Consumer.
Provides a simple script to verify messages are arriving in Kafka correctly.
"""

import json
import logging
from typing import List, Dict, Any

from kafka import KafkaConsumer
from kafka.errors import KafkaError

import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FraudKafkaConsumer:
    """
    Test consumer class to pull messages from the configured Kafka topic.
    """
    def __init__(self) -> None:
        """
        Initializes the Kafka consumer and connects to the broker specified in config.
        """
        try:
            self.consumer = KafkaConsumer(
                config.KAFKA_TOPIC,
                bootstrap_servers=config.KAFKA_BROKER,
                group_id=config.KAFKA_GROUP_ID,
                auto_offset_reset=config.KAFKA_AUTO_OFFSET_RESET,
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                consumer_timeout_ms=15000  # 15 seconds timeout
            )
            logger.info(f"Connected to Kafka broker at {config.KAFKA_BROKER} for topic '{config.KAFKA_TOPIC}'")
        except KafkaError as e:
            logger.error(f"Failed to connect to Kafka broker: {e}")
            raise

    def consume(self, max_messages: int = 10) -> List[Dict[str, Any]]:
        """
        Reads up to max_messages from the Kafka topic, prints them, and returns them.

        Args:
            max_messages (int): Maximum number of messages to consume.

        Returns:
            List[Dict[str, Any]]: A list of deserialized message dictionaries.
        """
        messages = []
        count = 0
        print(f"\n🎧 Waiting for messages on topic '{config.KAFKA_TOPIC}'...")

        try:
            for message in self.consumer:
                txn = message.value
                messages.append(txn)
                print(f"📥 Received: txn_id={txn.get('txn_id')} | user={txn.get('user_id')} | amount=${txn.get('amount')} | fraud={txn.get('is_fraud')}")

                count += 1
                if count >= max_messages:
                    break
        except Exception as e:
            logger.error(f"Error while consuming messages: {e}")

        print(f"🛑 Finished consuming {len(messages)} messages.")
        return messages

if __name__ == "__main__":
    try:
        consumer = FraudKafkaConsumer()
        consumer.consume(10)
    except Exception as e:
        print(f"Consumer failed: {e}")
