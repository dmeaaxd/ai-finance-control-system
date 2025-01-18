from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.authenticate import login_user, register_user, self
from app.db.database import get_db
from app.dtos.auth import UserLoginDto, UserRegisterDto, AccessTokenDto
from app.secure.security_config import apikey_scheme

auth_router = APIRouter()


@auth_router.post("/login", response_model=AccessTokenDto, status_code=201)
async def login(creds: UserLoginDto, db: AsyncSession = Depends(get_db)):
    return await login_user(db, creds)


@auth_router.post("/register", response_model=AccessTokenDto, status_code=201)
async def register(creds: UserRegisterDto, db: AsyncSession = Depends(get_db)):
    return await register_user(db, creds)


@auth_router.get("/self")
async def get_self(access_token: Annotated[str, Depends(apikey_scheme)], db: AsyncSession = Depends(get_db)):
    return await self(db, access_token)
