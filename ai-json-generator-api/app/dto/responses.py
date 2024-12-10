from pydantic import BaseModel


class TransactionalDetail(BaseModel):
    name: str
    price: int
    category: str


class ErrorResponse(BaseModel):
    error: int
    detail: str


class BasicResponse(BaseModel):
    result: dict
    total: float
