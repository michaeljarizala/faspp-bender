from decouple import config
from datetime import timedelta

HOST = config("HOST", default="0.0.0.0")
PORT = config("PORT", default="8000")
ROOT_PATH = config("ROOT_PATH", default="/")

# Database Configuration
DATABASE_URL = config(
    "DATABASE_URL", default="postgresql://user:password@localhost/dbname"
)
ASYNC_DATABASE_URL = config(
    "ASYNC_DATABASE_URL", default="postgresql+asyncpg://user:password@localhost/dbname"
)

# JWT Configuration
SECRET_KEY = config("SECRET_KEY")
REFRESH_SECRET_KEY = config("REFRESH_SECRET_KEY")
ALGORITHM = config("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", 1)
REFRESH_TOKEN_EXPIRE_DAYS = config("REFRESH_TOKEN_EXPIRE_DAYS", 1)

# Knox Configuration
KNOX_TOKEN_AUTH_CHARACTER_LENGTH = config("KNOX_TOKEN_AUTH_CHARACTER_LENGTH", 64, cast=int)
KNOX_TOKEN_EXPIRE_HOURS = config("KNOX_TOKEN_EXPIRE_HOURS", 8, cast=int)
KNOX_TOKEN_SECRET_KEY = config("KNOX_TOKEN_SECRET_KEY")
KNOX_TOKEN_KEY_LENGTH = config("KNOX_TOKEN_KEY_LENGTH", 8, cast=int)
KNOX_TOKEN_SALT_LENGTH = config("KNOX_TOKEN_SALT_LENGTH", 16, cast=int)
KNOX_TOKEN_TTL = timedelta(hours=config("KNOX_TOKEN_EXPIRE_HOURS", 8, cast=int))