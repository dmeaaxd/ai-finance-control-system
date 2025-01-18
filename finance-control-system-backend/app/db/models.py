from datetime import datetime

import pytz
from sqlalchemy import String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    pass


MoscowTZ = pytz.timezone("Europe/Moscow")


def moscow_now():
    return datetime.now(MoscowTZ)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    limit_mode: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    limit_sum: Mapped[int] = mapped_column(Integer, default=0)

    operations: Mapped[list["Operation"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    tokens: Mapped[list["Token"]] = relationship("Token", back_populates="user", cascade="all, delete-orphan")


class Token(Base):
    __tablename__ = "tokens"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    access_token: Mapped[str] = mapped_column(String, unique=True, index=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"))

    user: Mapped[User] = relationship("User", back_populates="tokens")


class Operation(Base):
    __tablename__ = "operations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    category: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=moscow_now, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    user: Mapped[User] = relationship(back_populates="operations")
