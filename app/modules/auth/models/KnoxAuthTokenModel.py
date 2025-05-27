import binascii

from datetime import timezone, datetime
from types import SimpleNamespace

from sqlalchemy import Column, String, DateTime, ForeignKey, func, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import SHA512

from app.utils.model import Base
from app.settings import KNOX_TOKEN_AUTH_CHARACTER_LENGTH, KNOX_TOKEN_TTL, KNOX_TOKEN_SALT_LENGTH
from app.modules.user.models.UserModel import User

class KnoxAuthToken(Base):
    __tablename__ = 'knox_authtoken'
    __table_args__ = {'schema': 'public'}

    digest = Column(String(128), primary_key=True)
    token_key = Column(String(8), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('public.auth_user.id'), nullable=False)
    created = Column(DateTime, default=func.now(), nullable=False)
    expiry = Column(DateTime, nullable=True)
    salt = Column(String(16), nullable=False)

KnoxAuthToken.user = relationship(User, foreign_keys=[KnoxAuthToken.user_id], primaryjoin=User.id == KnoxAuthToken.user_id, backref="knox_auth_token_user_id")