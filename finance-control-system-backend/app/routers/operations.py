from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.operations import get_all_operations_contr, get_operation_contr, \
    get_operations_by_categories_contr, create_operations_contr, update_operations_contr
from app.db.database import get_db
from app.dtos.operations import OperationDto
from app.secure.security_config import apikey_scheme

operations_router = APIRouter()


@operations_router.get("")
async def get_all_operations(access_token: Annotated[str, Depends(apikey_scheme)], db: AsyncSession = Depends(get_db)):
    return get_all_operations_contr(access_token, db)

@operations_router.get("/{operation_id}")
async def get_operation(operation_id: int, access_token: Annotated[str, Depends(apikey_scheme)], db: AsyncSession = Depends(get_db)):
    return get_operation_contr(operation_id, access_token, db)
@operations_router.get("")
async def get_operations_by_categories(categories: list[str], access_token: Annotated[str, Depends(apikey_scheme)], db: AsyncSession = Depends(get_db)):
    return get_operations_by_categories_contr(categories, access_token, db)

@operations_router.post("")
async def create_operations(operation: OperationDto, access_token: Annotated[str, Depends(apikey_scheme)], db: AsyncSession = Depends(get_db)):
    return create_operations_contr(operation, access_token, db)

@operations_router.put("/{operation_id}")
async def update_operations(operation_id: int, operation: OperationDto, access_token: Annotated[str, Depends(apikey_scheme)], db: AsyncSession = Depends(get_db)):
    return update_operations_contr(operation_id, operation, access_token, db)

