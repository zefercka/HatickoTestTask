from fastapi import FastAPI

from app.api.controllers.imei_controller import app as imei_controller
from app.api.controllers.auth_controller import app as auth_controller

app = FastAPI()

app.include_router(imei_controller, prefix='/api/imei', tags=['Imei'])
app.include_router(auth_controller, prefix='/api/auth', tags=['Auth'])