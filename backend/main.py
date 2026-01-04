import sys
import os

# Fix imports BEFORE any other imports
_BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_DIR = os.path.dirname(_BACKEND_DIR)
if _PROJECT_DIR not in sys.path:
    sys.path.insert(0, _PROJECT_DIR)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.auth import router as auth_router
from api.tasks import router as tasks_router
from utils.logging import setup_logging
import time
from collections import defaultdict

# Set up logging
setup_logging()

app = FastAPI(title="Todo API", version="1.0.0")

# Simple in-memory rate limiter (use Redis in production)
rate_limit_store = defaultdict(lambda: {"count": 0, "reset_time": 0})
RATE_LIMIT = 100  # requests per minute
RATE_LIMIT_WINDOW = 60  # seconds

def check_rate_limit(client_id: str) -> bool:
    """Check if client has exceeded rate limit."""
    current_time = time.time()
    if current_time > rate_limit_store[client_id]["reset_time"]:
        rate_limit_store[client_id] = {"count": 0, "reset_time": current_time + RATE_LIMIT_WINDOW}

    rate_limit_store[client_id]["count"] += 1
    return rate_limit_store[client_id]["count"] <= RATE_LIMIT

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware."""
    client_id = request.client.host
    if not check_rate_limit(client_id):
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests. Please try again later."}
        )
    response = await call_next(request)
    return response

@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    """Add security headers to responses."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development (frontend + server-side calls)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Create tables on startup
@app.on_event("startup")
def on_startup():
    from sqlmodel import SQLModel
    from database import engine
    SQLModel.metadata.create_all(engine)