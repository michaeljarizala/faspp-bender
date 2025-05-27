import base64
import hashlib
import hmac
import traceback

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""Get password hash"""


def get_password_hash(password):
    return pwd_context.hash(password)


"""Verify a bcrypt password"""


def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)


"""Verify a PBKDF2 Password"""


def verify_password_pbkdf2(plain_password: str, password: str) -> bool:
    try:
        algorithm, iterations, salt, hashed_password = password.split("$")

        if algorithm != "pbkdf2_sha256":
            return False

        iterations = int(iterations)

        derived_hash = hashlib.pbkdf2_hmac(
            "sha256", plain_password.encode(), salt.encode(), iterations, dklen=32
        )

        encoded_hash = base64.b64encode(derived_hash).decode()

        return hmac.compare_digest(encoded_hash, hashed_password)

    except Exception:
        traceback.print_exc()
        return False
