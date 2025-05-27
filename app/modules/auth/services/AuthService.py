import traceback

import jwt
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.utils.db.user import get_user_by_username
from app.utils.security.jwt import (create_access_token, create_refresh_token,
                                    renew_access_token)
from app.utils.security.password import verify_password_pbkdf2
from app.utils.security.knox import (create_knox_token)



def generate_token(db: Session, username: str, password: str, auth_mode: str = 'jwt'):
    if auth_mode == 'jwt':
        user = get_user_by_username(db, username)
        if user and verify_password_pbkdf2(password, user.password):
            access_token = create_access_token({"sub": username})
            refresh_token = create_refresh_token({"sub": username})

            return {
                "access": access_token,
                "refresh": refresh_token,
            }
    elif auth_mode == 'knox':
        user = get_user_by_username(db, username)
        if user and verify_password_pbkdf2(password, user.password):
            access_token = create_knox_token(db, user.id)

            return {"access": access_token, "refresh": ""}

    raise HTTPException(status_code=401, detail="Invalid credentials.")


def renew_token(token: str):
    try:
        new_token = renew_access_token(token)

        return {"access": new_token}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired.")
    except jwt.InvalidTokenError:
        traceback.print_exc()
        raise HTTPException(status_code=401, detail="Invalid refresh token.")

