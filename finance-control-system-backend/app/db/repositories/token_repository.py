import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Token, User


class TokenRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_or_update_token(self, user_id: int):
        query = select(Token).where(Token.user_id == user_id)
        result = await self.db_session.execute(query)
        existing_token = result.scalar_one_or_none()

        try:
            if existing_token:
                existing_token.access_token = str(uuid.uuid4())
                token = existing_token
            else:
                token = Token(
                    user_id=user_id,
                    access_token=str(uuid.uuid4())
                )
                self.db_session.add(token)

            await self.db_session.commit()
            await self.db_session.refresh(token)
            return token
        except IntegrityError:
            await self.db_session.rollback()
            return None

    async def get_user_by_token(self, token: str):
        subquery = select(Token.user_id).where(Token.access_token == token).scalar_subquery()
        query = select(User).where(User.id == subquery)
        result = await self.db_session.execute(query)
        user = result.scalar_one_or_none()

        return user
