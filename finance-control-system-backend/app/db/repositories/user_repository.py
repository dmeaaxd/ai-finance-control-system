from sqlalchemy import select, or_
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.dtos.auth import UserRegisterDto
from app.utils.pwd_hash import HashPassword


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def find_by_username(self, username: str) -> User | None:
        try:
            query = select(User).where(User.username == username)
            result = await self.db_session.execute(query)
            return result.scalar_one_or_none()
        except NoResultFound:
            return None

    async def find_by_username_or_telegram_id(self, username: str, telegram_id: int) -> User | None:
        try:
            query = select(User).where(or_(User.username == username, User.telegram_id == telegram_id))
            result = await self.db_session.execute(query)
            return result.scalar_one_or_none()
        except NoResultFound:
            return None

    async def find_by_id(self, user_id: int) -> User | None:
        try:
            query = select(User).where(User.id == user_id)
            result = await self.db_session.execute(query)
            return result.scalar_one_or_none()
        except NoResultFound:
            return None

    async def create_user(self, user_data: UserRegisterDto) -> User | None:
        hashed_password = HashPassword.hash(user_data.password)
        new_user = User(
            username=user_data.username,
            telegram_id=user_data.telegram_id,
            password=hashed_password
        )
        try:
            self.db_session.add(new_user)
            await self.db_session.commit()
            await self.db_session.refresh(new_user)
            return new_user
        except IntegrityError:
            await self.db_session.rollback()
            return None
