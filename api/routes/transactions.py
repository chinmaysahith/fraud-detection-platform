"""
Transaction history endpoints routes.
"""

from fastapi import APIRouter, Security, HTTPException, status
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from api.schemas import TransactionRecord
from api.auth import verify_api_key
from database.repository import TransactionRepository
from database.db import get_connection

router = APIRouter()

@router.get("/", response_model=list[TransactionRecord])
def get_transactions(
    limit: int = 10,
    api_key: str = Security(verify_api_key)
):
    """
    Returns most recent N transactions from PostgreSQL.
    """
    if limit > 100:
        limit = 100

    try:
        conn = get_connection()
        repo = TransactionRepository(conn)
        transactions = repo.get_recent_transactions(limit=limit)
        conn.close()
        return transactions
    except Exception as e:
        print(f"Database error while fetching transactions: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable."
        )

@router.get("/{txn_id}")
def get_transaction(
    txn_id: str,
    api_key: str = Security(verify_api_key)
):
    """
    Returns single transaction by ID.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM transactions WHERE txn_id = %s;", (txn_id,))
        row = cur.fetchone()

        if not row:
            cur.close()
            conn.close()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found."
            )

        columns = [desc[0] for desc in cur.description]
        transaction = dict(zip(columns, row))

        cur.close()
        conn.close()
        return transaction
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error while fetching transaction {txn_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable."
        )