from aiogram.types import Message
from ..dependecies.database import SessionLocal
from ..cruds import user_crud as crud


async def login_command(msg: Message):
    token = str(msg.text.split()[1:2][0])
    
    async with SessionLocal() as db:
        await crud.update_user_token(
            db, user_id=msg.from_user.id, new_token=token
        )
        await msg.answer('Токен сохранён', parse_mode='MarkdownV2')