"""
Stream simulator.
Continuously generates and streams transactions to the console.
"""

import sys
import time
import random

import config
from generator import User, TransactionGenerator

def main() -> None:
    """
    Main function to run the infinite transaction stream.
    """
    users = [User(f"user_{str(i).zfill(3)}") for i in range(1, config.NUM_USERS + 1)]

    print(f"🚀 Stream started | Users: {config.NUM_USERS} | Speed: {config.TRANSACTIONS_PER_SECOND} txns/sec")
    print("-" * 50)

    sleep_time = 1.0 / config.TRANSACTIONS_PER_SECOND

    try:
        while True:
            user = random.choice(users)
            generator = TransactionGenerator(user)

            prob = random.random()

            if prob < config.OBVIOUS_FRAUD_PROBABILITY:
                txn = generator.generate_obvious_fraud()
            elif prob < config.OBVIOUS_FRAUD_PROBABILITY + config.SUBTLE_FRAUD_PROBABILITY:
                txn = generator.generate_subtle_fraud()
            else:
                txn = generator.generate_normal()

            if txn["is_fraud"]:
                print(f"[FRAUD⚠️] txn_id: {txn['txn_id'][:6]} | user: {txn['user_id']} | amount: ${txn['amount']:.2f} | location: {txn['location']}")
            else:
                print(f"[NORMAL]  txn_id: {txn['txn_id'][:6]} | user: {txn['user_id']} | amount: ${txn['amount']:.2f} | location: {txn['location']}")

            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\n⏹️ Stream stopped gracefully.")
        sys.exit(0)

if __name__ == "__main__":
    main()
