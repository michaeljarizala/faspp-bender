from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


"""Response Schemas"""


class UserResponse(BaseModel):
    id: int
    username: str
