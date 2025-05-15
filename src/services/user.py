from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List, Optional
import base64
import json
import hmac
import hashlib
import time

from src.core.database import get_db
from src.core.security import SECRET_KEY, verify_password, get_password_hash
from src.models.user import User
from src.schemas.token import TokenPayload
from src.schemas.user import UserCreate, UserUpdate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class UserService:
    @staticmethod
    def get_user(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def create_user(db: Session, user_in: UserCreate) -> User:
        # Check if user exists
        if UserService.get_user_by_email(db, email=user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Create new user without is_active and is_superuser fields
        db_user = User(
            email=user_in.email,
            username=user_in.username,
            hashed_password=get_password_hash(user_in.password)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(db: Session, user_id: int, user_in: UserUpdate) -> Optional[User]:
        db_user = UserService.get_user(db, user_id)
        if not db_user:
            return None

        update_data = user_in.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )

        for field, value in update_data.items():
            setattr(db_user, field, value)

        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        db_user = UserService.get_user(db, user_id)
        if not db_user:
            return False

        db.delete(db_user)
        db.commit()
        return True

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        user = UserService.get_user_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
    ) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            # Simple token validation without jose
            # Format: base64(header).base64(payload).signature
            parts = token.split('.')
            if len(parts) != 3:
                raise credentials_exception
            
            # Decode payload
            try:
                payload_bytes = base64.urlsafe_b64decode(parts[1] + '=' * (4 - len(parts[1]) % 4))
                payload = json.loads(payload_bytes.decode('utf-8'))
            except Exception:
                raise credentials_exception
            
            # Check if token has expired
            if 'exp' in payload and payload['exp'] < time.time():
                raise credentials_exception
                
            # Verify signature
            message = f"{parts[0]}.{parts[1]}"
            signature = hmac.new(
                SECRET_KEY.encode(), 
                message.encode(), 
                hashlib.sha256
            ).digest()
            expected_signature = base64.urlsafe_b64encode(signature).decode('utf-8').rstrip('=')
            
            if not hmac.compare_digest(parts[2], expected_signature):
                raise credentials_exception
                
            # Get username from payload
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
                
            token_data = TokenPayload(sub=username)
        except Exception:
            raise credentials_exception

        user = UserService.get_user_by_username(db, username=token_data.sub)
        if user is None:
            raise credentials_exception
        return user
