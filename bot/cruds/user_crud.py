from app.logger import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user_model import User

from bot.config import constants


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    results = await db.execute(select(User).where(User.user_id == user_id))
    return results.scalars().first()


async def get_users(db: AsyncSession, limit: int = constants.ID_PER_PAGE, offset: int = 0) -> list[User] | None:
    results = await db.execute(select(User).offset(offset).limit(limit))
    return results.scalars().all()


async def add_user(db: AsyncSession, user_id: int, token: str | None = None, 
                   level_permission: int = 1) -> User:
    user = User(
        user_id=user_id, token=token, level_permission=level_permission
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user


async def update_user_token(db: AsyncSession, user_id: int, new_token: str) -> User | None:
    user = await get_user_by_id(db, user_id)
    
    if user is None:
        return None
    
    user.token = new_token
    await db.commit()
    await db.refresh(user)
    
    return user


async def are_users_exists(db: AsyncSession):
    results = await db.execute(select(User).limit(1))
    
    if results.scalars().first():
        return True
    
    return False


async def update_user_permission(db: AsyncSession, user_id: int, level_permission) -> User | None:
    user = await get_user_by_id(db, user_id)
    
    if user is None:
        return None

    if user.level_permission != level_permission:
        user.level_permission = level_permission
        await db.commit()
        await db.refresh(user)
    
    return user


async def delete_user(db: AsyncSession, user: User) -> None:
    await db.delete(user)
    await db.commit()
