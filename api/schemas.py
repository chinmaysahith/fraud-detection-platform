"""
Pydantic models for API request and response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TransactionRequest(BaseModel):
    """Input transaction for fraud prediction."""
    user_id: str = Field(..., example="user_042")
    amount: float = Field(..., example=250.00, gt=0)
    location: str = Field(..., example="New York")
    merchant: str = Field(..., example="grocery")
    device: str = Field(..., example="phone")
    time_of_day: str = Field(..., example="morning")
    day_of_week: str = Field(..., example="Monday")

class PredictionResponse(BaseModel):
    """Fraud prediction result."""
    txn_id: str
    user_id: str
    amount: float
    fraud_score: float
    label: str                    # SAFE / REVIEW / FRAUD
    is_fraud_predicted: bool
    prediction_threshold: float
    timestamp: str

class TransactionRecord(BaseModel):
    """Transaction record from database."""
    txn_id: str
    user_id: str
    amount: float
    location: str
    merchant: str
    fraud_score: float
    is_fraud_predicted: bool
    created_at: datetime

class FraudAlert(BaseModel):
    """Fraud alert record from database."""
    txn_id: str
    user_id: str
    amount: float
    location: str
    fraud_score: float
    alert_level: str
    created_at: datetime

class HealthResponse(BaseModel):
    """API health check response."""
    status: str
    model_loaded: bool
    database_connected: bool
    kafka_connected: bool
    version: str

class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: str