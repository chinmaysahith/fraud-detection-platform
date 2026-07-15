"""
Fraud alerts endpoints routes.
"""

from fastapi import APIRouter, Security, HTTPException, status
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from api.schemas import FraudAlert
from api.auth import verify_api_key
from database.repository import TransactionRepository
from database.db import get_connection

router = APIRouter()

@router.get("/", response_model=list[FraudAlert])
def get_fraud_alerts(
    limit: int = 10,
    level: Optional[str] = None,
    api_key: str = Security(verify_api_key)
):
    """
    Returns recent fraud alerts from PostgreSQL.
    """
    if limit > 100:
        limit = 100

    try:
        conn = get_connection()
        cur = conn.cursor()

        query = "SELECT * FROM fraud_alerts"
        params = []

        if level:
            query += " WHERE alert_level = %s"
            params.append(level)

        query += " ORDER BY created_at DESC LIMIT %s"
        params.append(limit)

        cur.execute(query, tuple(params))
        rows = cur.fetchall()

        columns = [desc[0] for desc in cur.description]
        alerts = [dict(zip(columns, row)) for row in rows]

        cur.close()
        conn.close()
        return alerts
    except Exception as e:
        print(f"Database error while fetching fraud alerts: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable."
        )