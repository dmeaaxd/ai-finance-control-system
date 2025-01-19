from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.token_repository import TokenRepository
from app.db.repositories.user_repository import UserRepository
from app.dtos.auth import UserLoginDto, AccessTokenDto
from app.utils.pwd_hash import HashPassword


async def login_user(db: AsyncSession, creds: UserLoginDto):
    user_repository = UserRepository(db)
    token_repository = TokenRepository(db)

    user = await user_repository.find_by_username(creds.username)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not HashPassword.verify(creds.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = await token_repository.create_or_update_token(user.id)

    response = AccessTokenDto(access_token=token.access_token)
    return response


async def register_user(db: AsyncSession, creds: UserLoginDto):
    user_repository = UserRepository(db)
    token_repository = TokenRepository(db)

    existing_user = await user_repository.find_by_username_or_telegram_id(creds.username, creds.telegram_id)

    if existing_user:
        if existing_user.username == creds.username:
            raise HTTPException(status_code=400, detail="Username already exists")
        if existing_user.telegram_id == creds.telegram_id:
            raise HTTPException(status_code=400, detail="Telegram ID already exists")

    new_user = await user_repository.create_user(creds)
    if new_user:
        token = await token_repository.create_or_update_token(new_user.id)
        response = AccessTokenDto(access_token=token.access_token)
        return response

    raise HTTPException(status_code=500, detail="Error while creating user")


async def self(db: AsyncSession, token: str):
    token_repository = TokenRepository(db)

    user = await token_repository.get_user_by_token(token)
    if user:
        return user

    raise HTTPException(status_code=401, detail="Unauthorized")
