from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.operation_repository import OperationRepository
from app.db.repositories.token_repository import TokenRepository
from app.dtos.operations import OperationDto


async def get_all_operations_contr(token: str, db: AsyncSession):
    token_repository = TokenRepository(db)
    operation_repository = OperationRepository(db)

    user = await token_repository.get_user_by_token(token)
    if user:
        operations = await operation_repository.get_all_operations(user_id=user.id)
        return operations

    raise HTTPException(status_code=401, detail="Unauthorized")


async def get_operation_contr(operation_id: int, token: str, db: AsyncSession):
    token_repository = TokenRepository(db)
    operation_repository = OperationRepository(db)

    user = await token_repository.get_user_by_token(token)
    if user:
        operation = await operation_repository.get_operation(user_id=user.id, operation_id=operation_id)
        return operation

    raise HTTPException(status_code=401, detail="Unauthorized")

async def get_operations_by_categories_contr(categories: list[str], token: str, db: AsyncSession):
    token_repository = TokenRepository(db)
    operation_repository = OperationRepository(db)

    user = await token_repository.get_user_by_token(token)
    if user:
        operations = await operation_repository.get_operations_by_categories(user_id=user.id, categories=categories)
        return operations

    raise HTTPException(status_code=401, detail="Unauthorized")


async def create_operations_contr(operation: OperationDto, token: str, db: AsyncSession):
    token_repository = TokenRepository(db)
    operation_repository = OperationRepository(db)

    user = await token_repository.get_user_by_token(token)
    if user:
        operation = await operation_repository.create_operation(user_id=user.id, operation=operation)
        return operation

    raise HTTPException(status_code=401, detail="Unauthorized")


async def update_operations_contr(operation_id: int, operation: OperationDto, token: str, db: AsyncSession):
    token_repository = TokenRepository(db)
    operation_repository = OperationRepository(db)

    user = await token_repository.get_user_by_token(token)
    if user:
        operation = await operation_repository.update_operation(user_id=user.id, operation_id=operation_id, operation=operation)
        return operation

    raise HTTPException(status_code=401, detail="Unauthorized")


