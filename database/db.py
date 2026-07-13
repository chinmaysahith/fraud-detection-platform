"""
Database connection and initialization module.
"""

import sys
import os
import psycopg2
from psycopg2.extensions import connection

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data import config

def get_connection() -> connection:
    """
    Returns a psycopg2 connection using configuration constants.
    Raises an error if the connection fails.
    """
    try:
        conn = psycopg2.connect(
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            dbname=config.POSTGRES_DB,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD
        )
        return conn
    except Exception as e:
        raise Exception(f"Failed to connect to the database: {e}")

def init_db() -> None:
    """
    Creates the 'transactions' and 'fraud_alerts' tables if they don't exist.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id              SERIAL PRIMARY KEY,
            txn_id          VARCHAR(100) UNIQUE NOT NULL,
            user_id         VARCHAR(50) NOT NULL,
            amount          FLOAT NOT NULL,
            location        VARCHAR(100),
            merchant        VARCHAR(100),
            device          VARCHAR(50),
            time_of_day     VARCHAR(50),
            day_of_week     VARCHAR(20),
            fraud_score     FLOAT NOT NULL,
            is_fraud_predicted BOOLEAN NOT NULL,
            fraud_type      VARCHAR(20),
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS fraud_alerts (
            id              SERIAL PRIMARY KEY,
            txn_id          VARCHAR(100) UNIQUE NOT NULL,
            user_id         VARCHAR(50) NOT NULL,
            amount          FLOAT NOT NULL,
            location        VARCHAR(100),
            fraud_score     FLOAT NOT NULL,
            alert_level     VARCHAR(20) NOT NULL,
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error initializing database tables: {e}")
    finally:
        cur.close()
        close_connection(conn)

def close_connection(conn: connection) -> None:
    """
    Closes the provided psycopg2 connection safely.
    """
    if conn is not None:
        try:
            conn.close()
        except Exception as e:
            print(f"Error closing connection: {e}")
