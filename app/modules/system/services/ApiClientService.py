from datetime import datetime
from collections import namedtuple

from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from fastapi import HTTPException

from app.modules.system.models.ApiClientModel import ApiClient
from app.modules.system.schemas import CreateApiClientSchema
from app.modules.user.models.UserModel import User


def get_api_clients(
    db: Session,
    offset: int = 0,
    limit: int = 10,
):
    Response = namedtuple("Response", ["count", "result",])

    filters = []
    
    query_paginated = db.query(Tag).filter(and_(*filters)).offset(offset).limit(limit)
    count = db.query(func.count(Tag.id)).filter(and_(*filters)).scalar()

    return Response(count=count, result=query_paginated.all())


def create_api_client(
    db: Session,
    api_client: CreateApiClientSchema,
):
    try:
        new_api_client = ApiClient(
            name=api_client.name,
            token=api_client.token,
        )

        db.add(new_api_client)
        db.flush()
        db.refresh(new_api_client)
        
        return new_api_client
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))