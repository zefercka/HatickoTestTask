from aiogram.types import Message
from bot.config import constants
from bot.logger import logger

from ..cruds import user_crud as crud
from ..dependecies.database import SessionLocal


async def delete_command(msg: Message):
    try:
        async with SessionLocal() as db:
            user = await crud.get_user_by_id(db, msg.from_user.id)
    except Exception as err:
        logger.error(err, exc_info=True)
        
    if not user:
        await msg.answer('У вас нет доступа к приложению')
        return
        
    if user.level_permission < constants.LEVEL_TO_ADD:
        await msg.answer('У вас нет доступа к действию')
    
    del_user = msg.text.split()[1:2]
    if len(del_user) == 0:
        await msg.answer(
            'Формат команды: ```tg /delete [id пользователя]```', parse_mode='MarkdownV2'
        )
        return
    
    if del_user[0].isdigit():
        try:
            async with SessionLocal() as db:
                user = await crud.get_user_by_id(db, user_id=int(del_user[0]))
                
                if user:
                    await crud.delete_user(db, user)
                    await msg.answer(
                        f'Пользователь с ID *{user.user_id}* больше не может пользоваться приложением',
                        parse_mode='MarkdownV2'
                    )
                    return
            
                await msg.answer(
                    f'Пользователь с ID *{del_user[0]}* не имеет доступа к приложению',
                    parse_mode='MarkdownV2'
                )
        except Exception as err:
            logger.error(err, exc_info=True)
    else:
        await msg.answer(
            f'ID пользователя должно быть числом', parse_mode='MarkdownV2'
        )
    