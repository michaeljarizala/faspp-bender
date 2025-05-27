from datetime import datetime
from collections import namedtuple

from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from fastapi import HTTPException

from app.modules.common.models.TagModel import Tag
from app.modules.common.schemas.TagSchema import CreateTagSchema
from app.modules.user.models.UserModel import User


def get_tags(
    db: Session,
    created_at: datetime | None = None,
    updated_at: datetime | None = None,
    created_by_id: int | None = None,
    offset: int = 0,
    limit: int = 10,
):
    Response = namedtuple("Response", ["count", "result",])

    filters = []

    if created_at:
        filters.append(Tag.created_at >= created_at)
    if updated_at:
        filters.append(Tag.updated_at >= updated_at)
    if created_by_id:
        filters.append(Tag.created_by_id == created_by_id)
    
    query_paginated = db.query(Tag).filter(and_(*filters)).offset(offset).limit(limit)
    count = db.query(func.count(Tag.id)).filter(and_(*filters)).scalar()

    return Response(count=count, result=query_paginated.all())


def create_tag(
    db: Session,
    tag: CreateTagSchema,
    actor: User,
):
    try:
        new_tag = Tag(
            name=tag.name,
            created_by_id=actor.id,
        )

        db.add(new_tag)
        db.flush()
        db.refresh(new_tag)

        # created_resource = db.query(Tag).filter(Tag.id == new_tag.id).first()
        

        # return created_resource
        return new_tag
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))