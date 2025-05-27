from typing import Optional
from types import SimpleNamespace

from fastapi import APIRouter, Query, Depends, Request
from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.core.pagination import paginate
from app.utils.schema.common_schema import APIPagedResponse, PaginationSchema, APISingleResponse, APIErrorResponse
from app.modules.common.schemas.TagSchema import TagSchema, CreateTagSchema
from app.modules.common.services.TagService import get_tags, create_tag
from app.utils.security.authentication import is_user_auth, is_user_or_api_client_auth

router = APIRouter(prefix="/v1/common", tags=["Tag"])

@router.get("/tags/", response_model=APIPagedResponse, description="""Retrieve list of tags - pagination implemented. This is a protected endpoint which may be authorized as a `user` or `API client`.""")
def load_tags(
    request: dict = Depends(is_user_or_api_client_auth),
    created_at: Optional[str] = Query(None, alias="Created At"),
    updated_at: Optional[str] = Query(None, alias="Updated At"),
    created_by_id: Optional[int] = Query(None, alias="Creator ID"),
    offset: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    query = get_tags(db, created_at, updated_at, created_by_id, offset, limit)
    content_categories = [TagSchema.model_validate(data, from_attributes=True) for data in query.result]
    
    return APIPagedResponse(
        success=True,
        message="Common tags have been fetched successfully!",
        data=content_categories,
        pagination=paginate(request.request, offset, limit, query)
    )


@router.post("/tags/", response_model=APISingleResponse|APIErrorResponse, description="""Creates a new tag and requires user token.""")
def post_tag(payload: CreateTagSchema, request: SimpleNamespace = Depends(is_user_auth), db: Session = Depends(get_db)):
    tag = create_tag(db, payload, request.actor)

    if tag.id:
        db.commit()
    
        return APISingleResponse(
            success=True,
            message="New tag has been created successfully!",
            data=TagSchema.model_validate(tag, from_attributes=True)
        )
    
    return APIErrorResponse(
        success=False,
        error={
            "code": 400,
            "message": "Unable to create new tag."
        }
    )