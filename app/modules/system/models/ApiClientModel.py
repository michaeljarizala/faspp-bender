from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.modules.user.models.UserModel import User
from app.utils.model import Base

class ApiClient(Base):
    __tablename__ = "api_client"
    __table_args__ = {"schema": "system"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    token = Column(String(32), unique=True, nullable=False) # API Token
    alias = Column(String(200), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))