from sqlalchemy.orm import Session

from app.modules.user.models.UserModel import User
from app.modules.user.schemas.UserSchema import UserCreate
from app.utils.security.password import get_password_hash


def create_user(db: Session, user: UserCreate):
    password = get_password_hash(user.password)
    db_user = User(username=user.username, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, id: str):
    return db.query(User).filter(User.id == id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()