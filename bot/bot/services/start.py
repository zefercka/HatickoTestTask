from aiogram.types import Message
from ..dependecies.database import SessionLocal
from ..cruds import user_crud as crud


async def start_command(msg: Message):
    async with SessionLocal() as db:
        if await crud.get_user_by_id(db, msg.from_user.id):
            await msg.answer('Выполните вход с помощью команды ```tg /login [токен]```', parse_mode='MarkdownV2')
        else:
            await msg.answer('У вас нет доступа к приложению')