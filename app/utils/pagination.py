from typing import Generic, TypeVar
from fastapi import Query
from pydantic import BaseModel


class PageParams(BaseModel):
    """Request query params for paginated API."""

    page: int = Query(ge=0, default=0)
    size: int = Query(ge=1, le=100)


T = TypeVar("T")


class PagedResponseSchema(BaseModel, Generic[T]):
    """Response schema for any paged API."""

    total: int
    page: int
    size: int
    results: list[T]
