from pydantic import BaseModel


class TokenCreate(BaseModel):
    username: str
    password: str


class TokenRefresh(BaseModel):
    token: str


"""Response Schemas"""


class TokenResponse(BaseModel):
    access: str
    refresh: str
