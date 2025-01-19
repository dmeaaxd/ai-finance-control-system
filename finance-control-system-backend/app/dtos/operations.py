from pydantic import BaseModel


class OperationDto(BaseModel):
    name: str
    price: int
    category: str

class Categories(BaseModel):
    categories: list[str]
