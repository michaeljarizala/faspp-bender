from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.user.models.UserModel import User


"""
=================================
User DB Utilities
=================================
"""
def get_user_by_email(db: Session = next(get_db()), email: str = None):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session = next(get_db()), username: str = None):
    return db.query(User).filter(User.username == username).first()