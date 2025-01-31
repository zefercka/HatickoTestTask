from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependecies.database import get_db
from ..schemas.auth_schema import Authorization, Registration
from ..schemas.user_schema import User
from ..services import auth_service

app = APIRouter()


@app.post("/login", response_model=User)
async def login(auth_form: Authorization, db: AsyncSession = Depends(get_db)):
    return await auth_service.authorize_user(db, auth_form)
    

@app.post("/register", response_model=User)
async def register(reg_form: Registration, db: AsyncSession = Depends(get_db)):
    return await auth_service.register_user(db, reg_form)