from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.modules.user.models.UserModel import User
from app.utils.model import Base


class Tag(Base):
    __tablename__ = "tag"
    __table_args__ = {"schema": "common"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))
    created_by_id = Column(Integer, ForeignKey("public.auth_user.id"))
    updated_by_id = Column(Integer, ForeignKey("public.auth_user.id"), nullable=True)




# Tag relationships
# use 'backref' in case of circular import issue e.g. backref="created_categories"
from app.modules.user.models.UserModel import User

Tag.created_by = relationship(User, foreign_keys=[Tag.created_by_id], primaryjoin=User.id == Tag.created_by_id, backref="tag_created_by")
Tag.updated_by = relationship(User, foreign_keys=[Tag.updated_by_id], primaryjoin=User.id == Tag.updated_by_id, backref="tag_updated_by")