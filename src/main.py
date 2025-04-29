from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1 import users, tasks

app = FastAPI(
    title="Score Management System",
    description="Backend API for Score Management System",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])