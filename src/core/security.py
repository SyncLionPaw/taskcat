from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
import base64
import json
import hmac
import hashlib
import time

SECRET_KEY = "YOUR_SECRET_KEY_HERE"  # In production, use a secure key and store in env vars
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    # Convert expire to timestamp for simpler serialization
    expire_timestamp = time.mktime(expire.timetuple())
    to_encode.update({"exp": expire_timestamp})
    
    # Create a simple JWT-like token
    # 1. Create header (typically algorithm info)
    header = {"alg": ALGORITHM, "typ": "JWT"}
    header_json = json.dumps(header, separators=(',', ':'))
    header_b64 = base64.urlsafe_b64encode(header_json.encode()).decode('utf-8').rstrip('=')
    
    # 2. Create payload
    payload_json = json.dumps(to_encode, separators=(',', ':'))
    payload_b64 = base64.urlsafe_b64encode(payload_json.encode()).decode('utf-8').rstrip('=')
    
    # 3. Create signature
    message = f"{header_b64}.{payload_b64}"
    signature = hmac.new(
        SECRET_KEY.encode(), 
        message.encode(), 
        hashlib.sha256
    ).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode('utf-8').rstrip('=')
    
    # 4. Combine all parts
    encoded_token = f"{header_b64}.{payload_b64}.{signature_b64}"
    
    return encoded_token
