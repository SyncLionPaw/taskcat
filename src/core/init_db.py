import sys
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.core.database import engine, Base, SessionLocal
from src.models.user import User  # 需要导入 User 模型才能创建表
from src.models.task import Task

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_default_users(db: Session):
    default_users = [
        {"username": "admin", "email": "admin@example.com", "password": "123"},
        {"username": "user", "email": "test@example.com", "password": "123"},
    ]

    for user_data in default_users:
        # 检查用户是否已存在
        existing_user = (
            db.query(User).filter(User.username == user_data["username"]).first()
        )
        if not existing_user:
            db_user = User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=pwd_context.hash(user_data["password"]),
            )
            db.add(db_user)
            print(f"Created default user: {user_data['username']}")

    db.commit()


def init_db():
    print("Database URL:", engine.url)  # 打印数据库连接信息
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully")
        # 创建默认用户
        db = SessionLocal()
        try:
            create_default_users(db)
        finally:
            db.close()
    except Exception as e:
        print(f"Error creating tables: {e}")


if __name__ == "__main__":
    for line in sys.path:
        print(line)
    print("Creating database tables...")
    init_db()
