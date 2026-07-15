"""
API key authentication module.
Protects all endpoints from unauthorized access.
"""
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.config import API_KEY, API_KEY_NAME

api_key_header = APIKeyHeader(
    name=API_KEY_NAME,
    auto_error=True
)

def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Verify the API key from request header.

    Args:
        api_key: API key from X-API-Key header

    Returns:
        api_key if valid

    Raises:
        HTTPException 403 if invalid
    """
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key. Access denied."
        )
    return api_key