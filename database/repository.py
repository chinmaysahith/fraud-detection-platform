"""
Database repository module for handling read/write operations.
"""

from typing import List, Dict, Any
from psycopg2.extensions import connection

class TransactionRepository:
    """
    Repository class for handling database operations for transactions and fraud alerts.
    """

    def __init__(self, conn: connection):
        """
        Initializes the repository with a psycopg2 connection.

        Args:
            conn (connection): A psycopg2 database connection.
        """
        self.conn = conn

    def save_transaction(self, txn: Dict[str, Any]) -> bool:
        """
        Inserts a transaction into the 'transactions' table.
        Handles duplicate txn_id gracefully using ON CONFLICT DO NOTHING.

        Args:
            txn (dict): The transaction dictionary containing data to save.

        Returns:
            bool: True on success, False on failure.
        """
        try:
            cur = self.conn.cursor()
            cur.execute(
                """
                INSERT INTO transactions (
                    txn_id, user_id, amount, location, merchant,
                    device, time_of_day, day_of_week, fraud_score,
                    is_fraud_predicted, fraud_type
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                ) ON CONFLICT (txn_id) DO NOTHING;
                """,
                (
                    txn.get("txn_id"),
                    txn.get("user_id"),
                    txn.get("amount"),
                    txn.get("location"),
                    txn.get("merchant"),
                    txn.get("device"),
                    txn.get("time_of_day"),
                    txn.get("day_of_week"),
                    txn.get("fraud_score", 0.0),
                    txn.get("is_fraud_predicted", False),
                    txn.get("fraud_type")
                )
            )
            self.conn.commit()
            cur.close()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error saving transaction: {e}")
            return False

    def save_fraud_alert(self, txn: Dict[str, Any]) -> bool:
        """
        Inserts a fraud alert into the 'fraud_alerts' table.
        Sets alert_level based on score (>= 0.8: 'FRAUD', >= 0.5: 'REVIEW').

        Args:
            txn (dict): The transaction dictionary containing data to save.

        Returns:
            bool: True on success, False on failure.
        """
        try:
            score = txn.get("fraud_score", 0.0)
            if score >= 0.8:
                alert_level = "FRAUD"
            elif score >= 0.5:
                alert_level = "REVIEW"
            else:
                return False  # Only called when score >= 0.5

            cur = self.conn.cursor()
            cur.execute(
                """
                INSERT INTO fraud_alerts (
                    txn_id, user_id, amount, location, fraud_score, alert_level
                ) VALUES (
                    %s, %s, %s, %s, %s, %s
                ) ON CONFLICT (txn_id) DO NOTHING;
                """,
                (
                    txn.get("txn_id"),
                    txn.get("user_id"),
                    txn.get("amount"),
                    txn.get("location"),
                    txn.get("fraud_score", 0.0),
                    alert_level
                )
            )
            self.conn.commit()
            cur.close()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error saving fraud alert: {e}")
            return False

    def get_recent_transactions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Returns the most recent N transactions.

        Args:
            limit (int): The number of transactions to return. Default is 10.

        Returns:
            list: A list of dictionaries representing the transactions.
        """
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT * FROM transactions ORDER BY created_at DESC LIMIT %s;",
                (limit,)
            )

            # Fetch column names
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()

            # Convert to list of dictionaries
            transactions = []
            for row in rows:
                transactions.append(dict(zip(columns, row)))

            cur.close()
            return transactions
        except Exception as e:
            print(f"Error fetching recent transactions: {e}")
            return []

    def get_fraud_alerts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Returns the most recent N fraud alerts.

        Args:
            limit (int): The number of fraud alerts to return. Default is 10.

        Returns:
            list: A list of dictionaries representing the fraud alerts.
        """
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT * FROM fraud_alerts ORDER BY created_at DESC LIMIT %s;",
                (limit,)
            )

            # Fetch column names
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()

            # Convert to list of dictionaries
            alerts = []
            for row in rows:
                alerts.append(dict(zip(columns, row)))

            cur.close()
            return alerts
        except Exception as e:
            print(f"Error fetching fraud alerts: {e}")
            return []
