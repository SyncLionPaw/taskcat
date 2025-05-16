"""
Script to check database schema for required columns
"""
import sys
import os
import sqlalchemy as sa
from sqlalchemy import inspect

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.database import engine

def check_task_table_columns():
    """Check if the tasks table has difficulty and points columns"""
    inspector = inspect(engine)
    columns = inspector.get_columns("tasks")
    column_names = [col["name"] for col in columns]
    
    print("Current columns in tasks table:", column_names)
    
    if "difficulty" not in column_names:
        print("WARNING: 'difficulty' column is missing from tasks table!")
        print("You may need to run the add_difficulty_points_to_tasks.sql migration")
    else:
        print("✓ 'difficulty' column exists")
        
    if "points" not in column_names:
        print("WARNING: 'points' column is missing from tasks table!")
        print("You may need to run the add_difficulty_points_to_tasks.sql migration")
    else:
        print("✓ 'points' column exists")

if __name__ == "__main__":
    check_task_table_columns()
