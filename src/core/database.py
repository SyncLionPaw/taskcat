from sqlalchemy import create_engine, text, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=True  # 开发环境打印SQL语句
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create all tables
def create_all_tables():
    Base.metadata.create_all(bind=engine)

# Function to check if column exists in table
def column_exists(table_name, column_name):
    inspector = inspect(engine)
    columns = [column['name'] for column in inspector.get_columns(table_name)]
    return column_name in columns

# Function to add missing columns to users table
def migrate_database():
    with engine.connect() as connection:
        # Check and add is_active column
        if not column_exists('users', 'is_active'):
            connection.execute(text("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE"))
            connection.commit()
            print("Added is_active column to users table")
        
        # Check and add is_superuser column
        if not column_exists('users', 'is_superuser'):
            connection.execute(text("ALTER TABLE users ADD COLUMN is_superuser BOOLEAN DEFAULT FALSE"))
            connection.commit()
            print("Added is_superuser column to users table")
        
        # Check and add created_at column
        if not column_exists('users', 'created_at'):
            connection.execute(text("ALTER TABLE users ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP"))
            connection.commit()
            print("Added created_at column to users table")
        
        # Check and add updated_at column
        if not column_exists('users', 'updated_at'):
            connection.execute(text("ALTER TABLE users ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
            connection.commit()
            print("Added updated_at column to users table")