from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1 import users, auth, tasks, ai  # Added ai import
from src.models.user import User
from src.models.material import Material
from src.models.task import Task  # Import models to register them

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
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"])  # Added ai router


@app.get("/")
def read_root():
    return {"message": "Welcome to Score Management System API"}