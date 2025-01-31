from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependecies.database import get_db
from ..schemas.imei_schema import ImeiCheck, ImeiInfo
from ..schemas.user_schema import User
from ..services import imei_service
from ..services.auth_service import get_current_user

app = APIRouter()


@app.post('', response_model=ImeiInfo)
async def check_imei(data: ImeiCheck, current_user: User = Depends(get_current_user)):
    response = await imei_service.check_imei(
        imei=data.imei
    )
    return response