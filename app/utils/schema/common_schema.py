from typing import Any, Optional, TypeVar, Generic

from pydantic import BaseModel

T= TypeVar("T")


class PaginationSchema(BaseModel):
    total_count: int
    previous: str | None
    next: str | None


class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

class APISingleResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str
    data: T | None

class APIPagedResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: list[T] | None
    pagination: PaginationSchema


class APIErrorResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    error: Any | None