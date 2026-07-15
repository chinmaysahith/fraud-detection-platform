"""
Fraud prediction endpoint route.
"""

from fastapi import APIRouter, Security, HTTPException, status
import uuid
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from api.schemas import TransactionRequest, PredictionResponse
from api.auth import verify_api_key
from model.predictor import FraudPredictor
from database.repository import TransactionRepository
from database.db import get_connection

router = APIRouter()

# Load predictor ONCE at module level
try:
    predictor = FraudPredictor()
except Exception as e:
    print(f"Warning: Failed to load FraudPredictor: {e}")
    predictor = None


@router.post("/", response_model=PredictionResponse)
def predict_fraud(
    transaction: TransactionRequest,
    api_key: str = Security(verify_api_key)
):
    """
    Predicts fraud for a given transaction.
    """
    if not predictor:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded."
        )

    try:
        # Generate unique txn_id using uuid4
        txn_id = str(uuid.uuid4())

        # Convert TransactionRequest to dict
        txn_dict = transaction.model_dump()
        txn_dict["txn_id"] = txn_id

        # Calls predictor.predict(txn_dict)
        scored_txn = predictor.predict(txn_dict)

        fraud_score = scored_txn.get("fraud_score", 0.0)

        # Label logic
        if fraud_score >= 0.8:
            label = "FRAUD"
        elif fraud_score >= 0.5:
            label = "REVIEW"
        else:
            label = "SAFE"

        scored_txn["label"] = label

        # Save result to PostgreSQL transactions table
        try:
            conn = get_connection()
            repo = TransactionRepository(conn)

            repo.save_transaction(scored_txn)

            # If score >= 0.5 -> also saves to fraud_alerts table
            if fraud_score >= 0.5:
                repo.save_fraud_alert(scored_txn)

            conn.close()
        except Exception as e:
            print(f"Database error while saving prediction: {e}")
            # still return prediction (log error)

        return PredictionResponse(
            txn_id=txn_id,
            user_id=scored_txn["user_id"],
            amount=scored_txn["amount"],
            fraud_score=fraud_score,
            label=label,
            is_fraud_predicted=scored_txn.get("is_fraud_predicted", False),
            prediction_threshold=0.8, # Hardcoded or from config if available
            timestamp=scored_txn.get("timestamp", "")
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {str(e)}"
        )