from typing import Optional, List
from types import SimpleNamespace

from fastapi import Request, Query
from urllib.parse import urlencode, urlparse, urlunparse

from sqlalchemy.sql.elements import BinaryExpression

from app.utils.schema.common_schema import PaginationSchema

class PaginationConfig(SimpleNamespace):
    def __init__(
        self,
        filters: Optional[List[BinaryExpression]] = None,
        offset: int = 0,
        limit: int = 10,
    ):
        super().__init__(
            filters=filters,
            offset=offset,
            limit=limit,
        )

def paginate(request: Request, offset: int, limit: int, query: Query):
    parsed_url = urlparse(str(request.url))
    https_base_url = urlunparse(("https", parsed_url.netloc, parsed_url.path, "", "", ""))
    
    previous_url = (
        f"{https_base_url}?{urlencode({'offset': max(0, offset - limit), 'limit': limit})}"
        if offset > 0 else None
    )
    next_url = (
        f"{https_base_url}?{urlencode({'offset': offset + limit, 'limit': limit})}"
        if (offset + limit) < query.count else None
    )

    return PaginationSchema(
        total_count=query.count,
        previous=previous_url,
        next=next_url
    )