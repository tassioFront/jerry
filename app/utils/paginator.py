
from app.schemas.pagination import PaginatedResponse
from sqlalchemy.orm import Query, Session
from typing import TypeVar
from math import ceil


T = TypeVar("T")

def paginate_query(
    *,
    query: Query,
    page: int,
    page_size: int,
    schema_cls: type[T],
) -> PaginatedResponse[T]:
    total = query.order_by(None).count()
    items = (
        query
        .limit(page_size)
        .offset((page - 1) * page_size)
        .all()
    )

    # If your schemas does not have from_attributes/orm_mode, it wont work:
    results = [schema_cls.model_validate(obj) for obj in items]

    total_pages = ceil(total / page_size) if page_size > 0 else 0

    return PaginatedResponse[T](
        total=total,
        page=page,
        page_size=page_size,
        results=results,
        total_pages=total_pages
    )
