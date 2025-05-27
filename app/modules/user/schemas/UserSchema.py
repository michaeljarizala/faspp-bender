from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str


class UserSchema(BaseModel):
    """
        Default Response Schema for User.
        Includes all fields and is recommended
        for use for endpoints intended to be
        viewed by the user itself instead of
        being accessible by other users.

        For example, the GET /v1/user/$ endpoint
        uses this response schema as the endpoint assumes
        that the same owner of the resource is the owner
        of the user itself.

        On the otherhand, GET /v1/user/{id}/ endpoint
        assumes that someone else is trying to access a user
        record with the specified user id. In this case,
        this response schema is not supposed to be used in order
        to restrict sensitive fields e.g. username
    """
    id: int
    username: str
    email: str
    last_login: datetime
    is_superuser: bool
    first_name: str
    last_name: str
    is_active: bool
    is_staff: bool
    date_joined: datetime

class PublicUserSchema(BaseModel):
    """
        Response schema for User resource intended
        for public viewing.

        This schema contains redacted and non-sensitive
        information only.
    """
    id: int
    first_name: str
    last_name: str