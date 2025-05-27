from pydantic import BaseModel, Field
from datetime import datetime


class ApiClientSchema(BaseModel):
    """
        Default schema for ApiClient.
        Recommended for use in write operations
        by superadmin users only.

        Can be used as a response schema
        for read operations by other users.
    """

    id: int
    name: str
    alias: str
    is_active: bool
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True


class CreateApiClientSchema(BaseModel):
    """
        Default schema for creating an instance of ApiClient.
    """

    id: int  = Field(default=None, description="Resource ID serial number", alias="id", read_only=True)
    name: str
    token: str
    alias: str
    created_at: datetime
    updated_at: datetime | None = None