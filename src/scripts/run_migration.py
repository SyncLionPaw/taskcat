import os
import sys
import logging
from pathlib import Path

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.database import engine
from sqlalchemy import text

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_migration(migration_file):
    """
    Run a SQL migration file against the database
    """
    migration_path = Path(__file__).parent.parent.parent / "migrations" / migration_file
    
    if not migration_path.exists():
        logger.error(f"Migration file not found: {migration_file}")
        return False
    
    try:
        with open(migration_path, "r") as f:
            sql = f.read()
        
        # Execute the SQL commands
        with engine.connect() as conn:
            logger.info(f"Running migration: {migration_file}")
            
            # Split by semicolon to execute multiple statements
            statements = sql.split(';')
            for statement in statements:
                if statement.strip():
                    conn.execute(text(statement))
            
            conn.commit()
            
        logger.info(f"Migration completed successfully: {migration_file}")
        return True
        
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Please provide a migration file name")
        sys.exit(1)
    
    migration_file = sys.argv[1]
    success = run_migration(migration_file)
    
    if not success:
        sys.exit(1)
