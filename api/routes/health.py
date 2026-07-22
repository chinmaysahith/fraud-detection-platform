"""
Health check endpoint route.
"""

from fastapi import APIRouter
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from api.schemas import HealthResponse
from data.config import MODEL_PATH, KAFKA_BROKER, API_VERSION, POSTGRES_HOST
from database.db import get_connection, close_connection

router = APIRouter()

@router.get("/", response_model=HealthResponse)
def health_check():
    """
    Returns API health check response.
    """
    model_loaded = os.path.exists(MODEL_PATH)

    # Check DB
    db_connected = False
    if not (os.environ.get("RENDER") == "true" and "localhost" in POSTGRES_HOST):
        try:
            # We already have fail-fast check in get_connection(), but let's be double safe
            conn = get_connection()
            close_connection(conn)
            db_connected = True
        except:
            db_connected = False

    # Check Kafka
    kafka_connected = False
    if not (os.environ.get("RENDER") == "true" and "localhost" in KAFKA_BROKER):
        try:
            from kafka import KafkaProducer
            # Add short timeouts in case of other environments
            p = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER, 
                request_timeout_ms=1000, 
                api_version_auto_timeout_ms=1000,
                max_block_ms=1000
            )
            p.close()
            kafka_connected = True
        except:
            kafka_connected = False

    return HealthResponse(
        status="healthy" if model_loaded and db_connected else "degraded",
        model_loaded=model_loaded,
        database_connected=db_connected,
        kafka_connected=kafka_connected,
        version=API_VERSION
    )