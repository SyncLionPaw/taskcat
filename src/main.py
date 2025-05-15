from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1 import users, auth
from src.core.database import create_all_tables, migrate_database
from src.models import User, Task  # Import models to register them

app = FastAPI(
    title="Score Management System",
    description="Backend API for the Score Management System",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

@app.on_event("startup")
def startup_event():
    """Create database tables and run migrations on startup"""
    create_all_tables()  # Create tables if they don't exist
    migrate_database()   # Add missing columns if needed

@app.get("/")
def read_root():
    return {"message": "Welcome to Score Management System API"}