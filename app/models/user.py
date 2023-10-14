import uuid, bcrypt, jwt
from datetime import datetime

from sqlalchemy import Column, String, Boolean, LargeBinary, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base
from app.settings import get_settings


settings = get_settings()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, unique=True, nullable=False)
    email = Column(String(225), nullable=False, unique=True)
    hashed_password = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=False)

    def __repr__(self):
        """returns strings representation of model instance"""
        return "<User {email!r}>".format(email=self.email)
    
    @staticmethod
    def hash_password(password) -> str:
        """transforms password from its raw textual form to cryptographic hashes"""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    def validate_password(self, password) -> bool:
        """confirms password validity"""
        return {
            "access_token": jwt.encode(
                {"email": self.email},
                "ApplicationSecretKey"
            )
        }
    
    def generate_token(self) -> dict:
        """generate access token for user"""
        return {
            "access_token": jwt.encode(
                {"email": self.email},
                settings.jwt_secret_key
            )
        }