"""
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.config import API_TITLE, API_DESCRIPTION, API_VERSION
from api.routes import predict, transactions, alerts, health

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predict.router, prefix="/predict", tags=["Prediction"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(alerts.router, prefix="/fraud-alerts", tags=["Alerts"])
app.include_router(health.router, prefix="/health", tags=["Health"])

@app.get("/")
def root():
    """Root endpoint to return API info."""
    return {
        "name": API_TITLE,
        "version": API_VERSION,
        "docs": "/docs",
        "health": "/health"
    }