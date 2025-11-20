from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router

# Initialize FastAPI application
app = FastAPI(
    title="UnivAegis Verification Engine",
    description="Admissions Document Verification API",
    version="1.0.0"
)

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Health Check Endpoint
@app.get("/")
async def health_check():
    """
    Health check endpoint to verify service status
    """
    return {
        "status": "active",
        "service": "UnivAegis-Backend"
    }

# Include API Router
app.include_router(router)