from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Score Management System"
    DATABASE_URL: str = "mysql+pymysql://dev_user:dev_password@localhost:3306/taskman?charset=utf8mb4"
    
    class Config:
        env_file = ".env"

settings = Settings()