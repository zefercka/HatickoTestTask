from datetime import date

from app.logger import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependecies import hash
from ..models.user_model import User


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    results = await db.execute(select(User).where(User.user_id == user_id))
    return results.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    results = await db.execute(select(User).where(User.username == username))
    return results.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    results = await db.execute(select(User).where(User.email == email))
    return results.scalars().first()


async def add_user(db: AsyncSession, username: str, email: str, password: str) -> User:
    password_hash = await hash.get_password_hash(password)
    user = User(
        username=username, email=email, password_hash=password_hash
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user


async def update_user_token(db: AsyncSession, user_id: int, new_token: str) -> User:
    user = await get_user_by_id(db, user_id)
    user.token = new_token
    await db.commit()
    await db.refresh(user)
    
    return user