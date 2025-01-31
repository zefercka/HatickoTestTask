from aiogram.types import Message
from bot.config import constants
from bot.logger import logger

from ..cruds import user_crud as crud
from ..dependecies.database import SessionLocal


async def add_command(msg: Message):
    try:
        async with SessionLocal() as db:
            user = await crud.get_user_by_id(db, msg.from_user.id)
            
        if not user:
            await msg.answer('У вас нет доступа к приложению')
            return
            
        if user.level_permission < constants.LEVEL_TO_ADD:
            await msg.answer('У вас нет доступа к действию')
        
        new_user = msg.text.split()[1:3]
        if len(new_user) == 0:
            await msg.answer('Формат команды: ```tg /add [id пользователя] [уровень доступа]```', parse_mode='MarkdownV2')
            return
        
        if new_user[0].isdigit() and new_user[1].isdigit():
            async with SessionLocal() as db:
                user = await crud.get_user_by_id(db, user_id=int(new_user[0]))
                
                if user:
                    user = await crud.update_user_permission(
                        db, user.user_id, level_permission=int(new_user[1])
                    )
                    await msg.answer(
                        f'Пользователь с ID *{user.user_id}* теперь имеет уровень доступа *{user.level_permission}*',
                        parse_mode='MarkdownV2'
                    )
                    return
                
                await crud.add_user(
                    db, user_id=int(new_user[0]), level_permission=int(new_user[1])
                )
            
                await msg.answer(
                    f'Пользователь с ID *{new_user[0]}* получил права доступа уровня *{new_user[1]}*',
                    parse_mode='MarkdownV2'
                )
        else:
            await msg.answer(f'ID пользователя и уровень доступа должны быть числами',
                            parse_mode='MarkdownV2')
    except Exception as err:
        logger.error(err, exc_info=True)
    