"""
    JWT utils for handling access and refresh tokens for user-based operations
    such as authenticating protected routes.
"""

from datetime import UTC, datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException

import jwt

from app.settings import (ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM,
                          REFRESH_SECRET_KEY, REFRESH_TOKEN_EXPIRE_DAYS,
                          SECRET_KEY)

from fastapi.security import APIKeyHeader

jwt_auth = APIKeyHeader(name="Authorization", auto_error=False, scheme_name="Access Token", description="Access token for protected resources.")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
        Use this function for creating an JWT access token.
    """

    to_encode = data.copy()
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    """
        Use this function for creating a JWT refresh token.
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)


def renew_access_token(token: str):
    """
        Use this function for renewing a given JWT token.
    """

    to_encode = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    """
        Use this function for decoding a given JWT token.

        Instead of using the jwt.decode function directly, we can call this function.
        This way, if we need to adjust the way the jwt.decode function is called, we
        can do so without changing potential several calls to the function. We only
        need to change the decode_token and the adjustments is carried out to whereever
        it is implemented.
    """
    
    if token:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired.")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token is invalid.")
    raise HTTPException(status_code=401, detail="Authentication credentials were not provided.")


def verify_access_token(token: str = Depends(jwt_auth)):
    """
        Verify a given JWT token, which for now, just simply calls the decode_token()
        function. One might ask why not simply use the decode_token function? Said
        function is solely used for decoding a given token without any additional logic.
        
        This function can or may be enhanced later if additional business logic is required.
    """
    if token:
        return decode_token(token)
    
    raise HTTPException(status_code=401, detail="Authentication credentials were not provided.")