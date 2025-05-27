from fastapi.security import APIKeyHeader

client_key_header = APIKeyHeader(name="X-Client-Key", auto_error=False, scheme_name="X-Client-Key", description="Key for API client-based requests.")
user_auth_header = APIKeyHeader(name="Authorization", auto_error=False, scheme_name="Knox/JWT Authorization", description="Authorization using JWT or Know. Use 'Bearer' prefix for JWT, and 'Token' for Knox.")