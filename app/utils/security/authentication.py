"""
    Utilities for handling authentication.
"""
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials
from types import SimpleNamespace

from app.settings import KNOX_TOKEN_AUTH_CHARACTER_LENGTH
from app.utils.security import client_key_header, user_auth_header
from app.utils.db.user import get_user_by_username
from app.utils.security.jwt import decode_access_token
from app.database import get_db
from app.utils.security.knox import authenticate_knox_token
from app.modules.system.models.ApiClientModel import ApiClient


def is_user_auth(
    request: Request,
    auth_header: HTTPAuthorizationCredentials = Depends(user_auth_header),
    db: Session = Depends(get_db)
):
    """
        Authenticate requests coming from a user-based request.

        Returns a dictionary with the following keys:
            - is_authenticated: A boolean indicating whether the request is authenticated.
            - actor: The actor object associated with the request, if authenticated.
    """

    scheme, token = "",""

    try:
        scheme, token = auth_header.split(' ')

    except Exception as e:
        raise HTTPException(status_code=401, detail="Authorization token is invalid.")

    if scheme == "Bearer":
        token = decode_access_token(token)
        user = get_user_by_username(db, username=token.get("sub"))

        if user and user.id:
            return SimpleNamespace(
                is_authenticated=True,
                actor=user,
                request=request
            )
        
        
        raise HTTPException(status_code=401, detail="Authorization token is invalid.")
        # return SimpleNamespace(
        #     is_authenticated=False,
        #     actor=None,
        #     request=request
        # )

    elif scheme == "Token":

        if token and (len(token) < KNOX_TOKEN_AUTH_CHARACTER_LENGTH or len(token) > KNOX_TOKEN_AUTH_CHARACTER_LENGTH):
            raise HTTPException(status_code=401, detail="Authorization token is invalid.")

        user = authenticate_knox_token(db, token=token)

        if user and user.id:
            return SimpleNamespace(
                is_authenticated=True,
                actor=user,
                request=request
            )
        
        
        return SimpleNamespace(
            is_authenticated=False,
            actor=None,
            request=request
        )

    raise HTTPException(status_code=401, detail="Authorization token is invalid or missing.")


def is_user_or_api_client_auth(
    request: Request,
    auth_header = Depends(user_auth_header),
    client_key_header: str = Depends(client_key_header),
    db: Session = Depends(get_db)
):
    """
        Authenticate requests coming from an actor (user or API client).

        Returns a dictionary with the following keys:
            - is_authenticated: A boolean indicating whether the request is authenticated.
            - actor: The actor object associated with the request, if authenticated.
    """

    if auth_header:
       
        scheme, token = "",""

        try:
            scheme, token = auth_header.split(' ')

        except Exception as e:
            raise HTTPException(status_code=401, detail="Authorization token is invalid.")

        if scheme == "Bearer":
            token = decode_access_token(token)
            user = get_user_by_username(db, username=token.get("sub"))

            if user and user.id:
                return SimpleNamespace(
                    is_authenticated=True,
                    actor=user,
                    request=request
                )
        
        
            return SimpleNamespace(
                is_authenticated=False,
                actor=None,
                request=request
            )

        elif scheme == "Token":

            if token and (len(token) < KNOX_TOKEN_AUTH_CHARACTER_LENGTH or len(token) > KNOX_TOKEN_AUTH_CHARACTER_LENGTH):
                raise HTTPException(status_code=401, detail="Authorization token is invalid.")
                
            user = authenticate_knox_token(db, token=token)

            if user and user.id:
                user = get_user_by_username(db, username=user.username)

                return SimpleNamespace(
                    is_authenticated=True,
                    actor=user,
                    request=request
                )
        
        
            return SimpleNamespace(
                is_authenticated=False,
                actor=None,
                request=request
            )

    if client_key_header:
        # TODO: Before reaching the return block, verify the client key by looking it up in the database: system.api_client (ApiClient model)
        # In the future, an RBAC operation must be performed to ensure the client has the necessary permissions before granting the request.

        api_client = db.query(ApiClient).filter(ApiClient.token == client_key_header, ApiClient.is_active == True).first()

        if not api_client or (api_client and api_client.id == None):
            raise HTTPException(status_code=401, detail="Authorization token is invalid.")

        return SimpleNamespace(
            is_authenticated=True,
            request=request
        )

    raise HTTPException(status_code=401, detail="Authorization credentials are missing.")