import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from src.core.database import create_all_tables, migrate_database
from src.models import User, Task  # Import models to register them

if __name__ == "__main__":
    print("Creating database tables...")
    create_all_tables()
    print("Running database migrations...")
    migrate_database()
    print("Database setup completed successfully!")
