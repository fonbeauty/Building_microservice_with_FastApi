from pydantic import BaseModel
from typing import List
from models.user import User


class PaginatedResponse(BaseModel):
    items: List[User]
    total: int
    page: int
    size: int
    pages: int
