from datetime import datetime, timedelta, timezone

import jwt
from app.config import constants, settings


async def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=constants.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.ACCESS_SECRET_KEY, algorithm=constants.JWT_ALGORITHM)
    return token


async def get_payload(token: str) -> dict:
    return jwt.decode(
        jwt=token, 
        key=settings.ACCESS_SECRET_KEY, 
        algorithms=[constants.JWT_ALGORITHM]
    )


async def get_user_id(token: str) -> int:
    payload = await get_payload(token)
    user_id = payload.get("sub")
    return int(user_id)


async def get_expire_date(token: str) -> datetime:
    payload = await get_payload(token)
    expire_date = payload.get("exp")
    return expire_date