from pydantic import BaseModel
from typing import List


class ErrorDetail(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: List[ErrorDetail]
