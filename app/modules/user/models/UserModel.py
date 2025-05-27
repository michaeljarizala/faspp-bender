from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData
from app.utils.model import Base

# metadata = MetaData(schema="public")  # Define schema
# Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = "auth_user"
    __table_args__ = {"schema": "public"}  # Explicit schema declaration

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    last_login = Column(DateTime, nullable=True)
    is_superuser = Column(Boolean)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean)
    is_staff = Column(Boolean)
    date_joined = Column(DateTime)