import re

from app.api.dependecies.database import get_db
from app.api.dependecies.exceptions import (InternalServerError,
                                            InvalidToken, TokenExpired,
                                            UserNotFound, TokenRevoked)
from app.api.schemas.auth_schema import Authorization, Registration
from app.api.schemas.user_schema import User
from app.logger import logger
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from jwt import InvalidTokenError
from jwt.exceptions import DecodeError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from ..cruds import user_crud as crud
from ..dependecies import hash, jwt

token_key = APIKeyHeader(name="Authorization")

async def authorize_user(db: AsyncSession, data: Authorization) -> User:
    user = await authenticate_user(db, data.login, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
        
    try:
        access_token = await jwt.create_access_token(data={"sub": str(user.user_id)})
        
        user = await crud.update_user_token(
            db, user_id=user.user_id, new_token=access_token
        )

        user = User.model_validate(user)
    except Exception as err:
        logger.error(err, exc_info=True)
        raise InternalServerError
    
    return user


async def register_user(db: AsyncSession, registration_form: Registration) -> User:
    try:
        is_unique_user = \
            False if await crud.get_user_by_email(db, registration_form.email) or \
            await crud.get_user_by_username(db, registration_form.username) else True
    except Exception as err:
        logger.error(err, exc_info=True)
        raise InternalServerError
    
    if is_unique_user is False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user already exists",
        )
    
    try:
        user = await crud.add_user(db, **registration_form.model_dump())

        data = Authorization(login=registration_form.email, password=registration_form.password)
        user = await authorize_user(db, data)
        
        return user
    except Exception as err:
        logger.error(err, exc_info=True)
        raise InternalServerError
 

async def authenticate_user(db: AsyncSession, login: str, 
                            password: str) -> User | None:
    
    try:
        user = \
            await crud.get_user_by_username(db, username=login) or \
            await crud.get_user_by_email(db, email=login)
        if user is None:
            return None

        if await hash.verify_password(password, user.password_hash):
            return User.model_validate(user)
        
        return None
    except Exception as err:
        logger.error(err, exc_info=True)
        raise InternalServerError


async def get_current_token(auth_key: str = Security(token_key)) -> str:
    token = auth_key.split()[-1]
    return token


async def get_current_user(db: AsyncSession = Depends(get_db), 
                           token: str = Depends(get_current_token)) -> User:    
    try:
        user_id = await jwt.get_user_id(token=token)            
        user = await crud.get_user_by_id(db, user_id=user_id)
        
        if user is None:
            raise UserNotFound
        
        if user.token != token:
            raise TokenRevoked
        
        return User.model_validate(user)
        
    except ExpiredSignatureError:
        raise TokenExpired
    except DecodeError:
        raise InvalidToken
    except InvalidTokenError as err:
        logger.error(err, exc_info=True)
        raise InternalServerError