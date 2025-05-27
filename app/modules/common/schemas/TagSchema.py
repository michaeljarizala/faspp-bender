from pydantic import BaseModel, Field
from datetime import datetime

from app.modules.user.schemas.UserSchema import PublicUserSchema


class TagSchema(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime | None

    # read fields
    created_by: PublicUserSchema = Field(default=None, description="Creator of this resource", alias="created_by", read_only=True)
    updated_by: PublicUserSchema | None = Field(default=None, description="Updater of this resource", alias="updated_by", read_only=True)

    # write fields
    created_by_id: int = Field(default=None, description="Creator of this resource", alias="created_by_id", write_only=True, exclude=True)
    updated_by_id: int | None = Field(default=None, description="Updater of this resource", alias="updated_by_id", write_only=True, exclude=True)

    class Config:
        from_attributes = True


class CreateTagSchema(BaseModel):
    """
        Default schema for creating a Tag.
    """

    # id: int  = Field(default=None, description="Resource ID serial number", alias="id", read_only=True)
    name: str
    updated_at: datetime | None = None

    # write fields
    created_by: int = Field(default=None, description="Creator of this resource", alias="created_by", write_only=True, exclude=True)
    updated_by: int | None = Field(default=None, description="Updater of this resource", alias="updated_by", write_only=True, exclude=True)

    class Config:
        from_attributes = True