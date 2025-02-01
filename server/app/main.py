from app.api.controllers.auth_controller import app as auth_controller
from app.api.controllers.health_controller import app as health_controller
from app.api.controllers.imei_controller import app as imei_controller
from fastapi import FastAPI

app = FastAPI()

app.include_router(imei_controller, prefix='/api/imei', tags=['Imei'])
app.include_router(auth_controller, prefix='/api/auth', tags=['Auth'])
app.include_router(health_controller, prefix='/api/health', tags=['Health'])