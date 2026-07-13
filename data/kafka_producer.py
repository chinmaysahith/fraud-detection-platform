"""
Kafka Producer wrapper.
Provides a class to serialize and send transaction data to a Kafka topic.
"""

import json
import logging
from typing import Dict, Any, Optional

from kafka import KafkaProducer
from kafka.errors import KafkaError

import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FraudKafkaProducer:
    """
    Kafka Producer class that handles connecting to the broker and sending transactions.
    """
    def __init__(self) -> None:
        """
        Initializes the Kafka producer and connects to the broker specified in config.
        If the connection fails, self.producer is set to None.
        """
        self.producer: Optional[KafkaProducer] = None
        try:
            # We explicitly check the connection status to gracefully fallback
            # and not crash the startup of the stream loop.
            import socket
            host, port = config.KAFKA_BROKER.split(':')
            socket.create_connection((host, int(port)), timeout=2).close()

            self.producer = KafkaProducer(
                bootstrap_servers=config.KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                api_version=(2, 5, 0),
                request_timeout_ms=5000,
                max_block_ms=5000
            )
            logger.info(f"Connected to Kafka broker at {config.KAFKA_BROKER}")
        except Exception as e:
            logger.warning(f"Failed to connect to Kafka broker at {config.KAFKA_BROKER}: {e}")
            print(f"Warning: Kafka is not running or unreachable at {config.KAFKA_BROKER}. Proceeding with console output only.")

    def send_transaction(self, txn: Dict[str, Any]) -> bool:
        """
        Serializes and sends a transaction dictionary to the configured Kafka topic.

        Args:
            txn (Dict[str, Any]): The transaction dictionary to send.

        Returns:
            bool: True if sent successfully, False otherwise.
        """
        if not self.producer:
            return False

        try:
            future = self.producer.send(config.KAFKA_TOPIC, value=txn)
            # block for 'synchronous' sends to ensure message was sent
            _ = future.get(timeout=10)
            return True
        except KafkaError as e:
            logger.error(f"Failed to send transaction {txn.get('txn_id')} to Kafka: {e}")
            return False

    def close(self) -> None:
        """
        Flushes remaining messages and closes the Kafka producer connection.
        """
        if self.producer:
            try:
                self.producer.flush()
                self.producer.close()
                logger.info("Kafka producer closed cleanly.")
            except Exception as e:
                logger.error(f"Error closing Kafka producer: {e}")
