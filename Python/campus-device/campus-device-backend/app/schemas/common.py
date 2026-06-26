from pydantic import BaseModel
from typing import Any, Optional, List, Generic, TypeVar

T = TypeVar("T")


class PaginatedResponse(BaseModel):
    list: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int