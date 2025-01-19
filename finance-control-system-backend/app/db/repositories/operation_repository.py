from select import select
from typing import Any, List, Sequence

from sqlalchemy import Row, RowMapping
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Operation
from app.dtos.operations import OperationDto


class OperationRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_operations(self, user_id: int) -> Sequence[Row[Any] | RowMapping | Any] | list[Any]:
        try:
            query = select(Operation).where(Operation.user_id == user_id)
            result = await self.db_session.execute(query)
            return result.scalars().all()
        except NoResultFound:
            return []

    async def get_operation(self, user_id: int, operation_id: int) -> Operation | None:
        try:
            query = select(Operation).where(
                Operation.user_id == user_id,
                Operation.id == operation_id
            )
            result = await self.db_session.execute(query)
            return result.scalar_one_or_none()
        except NoResultFound:
            return None

    async def get_operations_by_categories(self, user_id: int, categories: list[str]):
        try:
            query = select(Operation).where(
                Operation.user_id == user_id,
                Operation.category.in_(categories)
            )
            result = await self.db_session.execute(query)
            return result.scalars().all()
        except NoResultFound:
            return []

    async def create_operation(self, user_id: int, operation: OperationDto) -> Operation | None:
        new_operation = Operation(
            name=operation.name,
            price=operation.price,
            category=operation.category,
            user_id=user_id,
        )
        try:
            self.db_session.add(new_operation)
            await self.db_session.commit()
            await self.db_session.refresh(new_operation)
            return new_operation
        except IntegrityError:
            await self.db_session.rollback()
            return None
        except Exception:
            await self.db_session.rollback()
            return None

    async def update_operation(self, user_id: int, operation_id: int, operation: OperationDto) -> Operation | None:
        try:
            query = select(Operation).where(Operation.id == operation_id, Operation.user_id == user_id)
            result = await self.db_session.execute(query)
            existing_operation = result.scalar_one_or_none()

            if existing_operation:
                existing_operation.name = operation.name
                existing_operation.price = operation.price
                existing_operation.category = operation.category
                await self.db_session.commit()
                await self.db_session.refresh(existing_operation)
                return existing_operation
            else:
                return None
        except IntegrityError:
            await self.db_session.rollback()
            return None
        except Exception:
            await self.db_session.rollback()
            return None
