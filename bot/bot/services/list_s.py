from aiogram.types import Message
from bot.config import constants

from ..cruds import user_crud as crud
from ..dependecies.database import SessionLocal


async def list_command(msg: Message):
    async with SessionLocal() as db:
        user = await crud.get_user_by_id(db, msg.from_user.id)
        
    if not user:
        await msg.answer('У вас нет доступа к приложению')
        return
        
    if user.level_permission < constants.LEVEL_TO_ADD:
        await msg.answer('У вас нет доступа к действию')
    
    list_number = msg.text.split()[1:2]
    if len(list_number) == 0:
        await msg.answer(
            'Формат команды: ```tg /list [номер страницы]```', parse_mode='MarkdownV2'
        )
        return
    
    if list_number[0].isdigit():
        list_number = int(list_number[0])
        users = await crud.get_users(db, offset=constants.ID_PER_PAGE * (list_number - 1))
        print(users)
        answer_msg = \
            "ID           \| Доступ \n"
        
        for user in users:
            answer_msg += f"{str(user.user_id).ljust(12)} \| {user.level_permission} \n"
        
        await msg.answer(answer_msg, parse_mode='MarkdownV2')
        
    else:
        await msg.answer(
            f'Номер страницы должен быть числом', parse_mode='MarkdownV2'
        )
    