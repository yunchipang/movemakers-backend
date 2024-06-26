from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from app.settings import get_settings

settings = get_settings()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """hashes a password using bcrypt."""
    return pwd_context.hash(plain_password)


def validate_password(plain_password, hashed_password) -> bool:
    """confirms password validity."""
    return pwd_context.verify(plain_password, hashed_password)


def generate_token(data: dict, expires_delta: timedelta | None = None):
    """generates a jwt token or extends its expiration time"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt
