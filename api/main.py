"""
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.config import API_TITLE, API_DESCRIPTION, API_VERSION
from api.routes import predict, transactions, alerts, health, mlops

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

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Include routers
app.include_router(predict.router, prefix="/predict", tags=["Prediction"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(alerts.router, prefix="/fraud-alerts", tags=["Alerts"])
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(mlops.router, prefix="/mlops", tags=["MLOps"])

# Mount static files to serve the built React frontend
frontend_dist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/dist'))

if os.path.exists(frontend_dist_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist_path, "assets")), name="static")

    @app.get("/{catchall:path}")
    def serve_frontend(catchall: str = ""):
        # Prevent intercepting API documentation / docs routes
        if catchall in ["docs", "redoc", "openapi.json"]:
            raise HTTPException(status_code=404)
        index_file = os.path.join(frontend_dist_path, "index.html")
        return FileResponse(index_file)
else:
    @app.get("/")
    def root():
        """Root endpoint to return API info."""
        return {
            "name": API_TITLE,
            "version": API_VERSION,
            "docs": "/docs",
            "health": "/health"
        }