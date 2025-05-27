import os
import binascii
import hmac

from os import urandom as generate_bytes

from types import SimpleNamespace
from datetime import UTC, datetime, timezone

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import SHA512

from fastapi import Depends

from sqlalchemy.orm import Session

from app.utils.security import user_auth_header
from app.modules.auth.models.KnoxAuthTokenModel import KnoxAuthToken, User
from app.settings import KNOX_TOKEN_KEY_LENGTH, KNOX_TOKEN_AUTH_CHARACTER_LENGTH, KNOX_TOKEN_TTL, KNOX_TOKEN_SALT_LENGTH

# knox_auth = APIKeyHeader(name="Authorization", auto_error=False, scheme_name="Knox Access Token", description="Access token for protected resources using Knox.")

def create_knox_token(db: Session, user_id: int):
    """
    Creates a new Knox token for the given user.
    """

    # Generate a random token
    knox = create_token()

    # Extract first 8 chars for token_key
    token_key = knox.token[:KNOX_TOKEN_KEY_LENGTH]

    # Generate a random salt
    # salt = binascii.hexlify(os.urandom(KNOX_TOKEN_SALT_LENGTH)).decode()

    # Hash the token with salt
    digest = hash_token(knox.token, knox.salt)

    # Create the token entry in DB
    auth_token = KnoxAuthToken(
        digest=digest, token_key=token_key, salt=knox.salt, user_id=user_id, expiry=knox.expiry
    )

    db.add(auth_token)
    db.commit()

    # Return the full token (client stores this)
    return knox.token

def authenticate_knox_token(db: Session, token: str = Depends(user_auth_header)):
    """
    Authenticates a user based on a given Knox token.
    """
    if not token or len(token) < 8:
        return None  # Invalid token

    # Extract the first 8 characters (token key) for lookup
    token_key = token[:8]

    # Fetch the corresponding KnoxAuthToken entry
    auth_token = db.query(KnoxAuthToken).filter(KnoxAuthToken.token_key == token_key).first()

    if not auth_token or not auth_token.salt:
        return None  # No matching token found

    # Verify token by rehashing it with the stored salt
    expected_digest = hash_token(token, auth_token.salt)

    if not hmac.compare_digest(expected_digest, auth_token.digest):
        return None  # Invalid token

    # Check for expiration
    if auth_token.expiry and auth_token.expiry < datetime.now(timezone.utc):
        return None  # Token expired

    # Retrieve the associated user
    user = db.query(User).filter(User.id == auth_token.user_id).first()

    return user  # Return the authenticated user





def create_token_string():
    return binascii.hexlify(
        generate_bytes(int(KNOX_TOKEN_AUTH_CHARACTER_LENGTH / 2))
    ).decode()

def create_salt_string():
    return binascii.hexlify(
    generate_bytes(int(KNOX_TOKEN_SALT_LENGTH / 2))).decode()

def create_token(expiry=KNOX_TOKEN_TTL):
    token = create_token_string()
    salt = create_salt_string()
    digest = hash_token(token, salt)

    if expiry is not None:
        expiry = datetime.now(timezone.utc) + expiry

    return SimpleNamespace(
        token=token,
        digest=digest,
        salt=salt,
        expiry=expiry
    )

def hash_token(token, salt):
    """
        This function aims to verify the integrity and validity of a token.
        This function is adopted from the knox Python library, particularly
        the `hash_token` function at knox.crypto.py.
    """

    digest = hashes.Hash(SHA512(), backend=default_backend())
    digest.update(binascii.unhexlify(token))
    digest.update(binascii.unhexlify(salt))
    return binascii.hexlify(digest.finalize()).decode()