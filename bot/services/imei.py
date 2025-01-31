import json
import re
from datetime import datetime

import requests
from aiogram.types import Message, InputFile
from bot.config import constants
from bot.logger import logger

from ..cruds import user_crud as crud
from ..dependecies.database import SessionLocal

status_to_word = {
    True: 'Да',
    False: 'Нет',
    None: '-'
}

fmi_status = {
    True: 'Включено',
    False: 'Выключено',
    None: '-'
}


async def imei_command(msg: Message):
    try:
        async with SessionLocal() as db:
            user = await crud.get_user_by_id(db, msg.from_user.id)
    except Exception as err:
        logger.error(err, exc_info=True)
        
        await msg.answer('Сервис временно недоступен')
        return
        
    if not user:
        await msg.answer('У вас нет доступа к приложению')
        return
        
    if user.token is None:
        await msg.answer(
            'Выполните вход с помощью команды ```tg /login [токен]```', 
            parse_mode='html'
        )
        return
    
    imei = str(msg.text.split()[1:2][0])
    
    if len(imei) < 8 or len(imei) > 15:
        await msg.answer('IMEI должен стоять из 8-15 символов')
        return

    await msg.answer('Запрос в обработке')

    headers = {
        'Authorization': f'Bearer {user.token}',
        'Content-Type': 'application/json',
    }
    
    body = {
        'imei': imei
    }
    
    try:
        response = requests.post(
            url=f"{constants.BASE_API_URL}{constants.IMEI_API_ROUTE}",
            data=json.dumps(body),
            headers=headers
        )
    except Exception as err:
        logger.error(err, exc_info=True)
        
        await msg.answer('Сервис временно недоступен')
        return
        
    if response.status_code in [500, 502]:
        await msg.answer(r'Сервис временно недоступен\. Попробуйте позже', parse_mode='MarkdownV2')
    elif response.status_code in [404, 401]:
        await msg.answer(r'Токен более недействителен\. Обновите его с помощью команды \
            ```tg /login [токен]```', parse_mode='MarkdownV2')
    elif response.status_code == 200:
        data = json.loads(response.text)
        answer_msg = \
        f"""
            Имя устройства: {data['device_name'] if data['device_name'] else '-'}
            IMEI: {data['imei'] if data['imei'] else '-'}
            MEID: {data['meid'] if data['meid'] else '-'}
            IMEI2: {data['imei2'] if data['imei2'] else '-'}
            Серийный номер: {data['serial'] if data['serial'] else '-'}
            Время покупки: {
                datetime.fromtimestamp(data['est_purchase_date']) \
                    if data['est_purchase_date'] else '-'
            } (UTC)
            Блокировка сим-карты: {
                status_to_word[data['sim_lock']] \
                    if data['sim_lock'] is not None else '-'
            }
            Гарантия: {data['warranty_status']}
            Тех. поддержка: {
                status_to_word[data['technical_support']] \
                    if data['technical_support'] is not None else '-'
            }
            Описание: {data['model_desc'] if data['model_desc'] else '-'} 
            Страна покупки: {data['purchase_country'] if data['purchase_country'] else '-'}
            Регион Appple: {data['apple_region'] if data['apple_region'] else '-'}
            Найти iPhone: {
                fmi_status[data['fmi_on']] \
                    if data['fmi_on'] is not None else '-'
            }
            Lost Mode: {
                fmi_status[data['lost_mode']] \
                    if data['lost_mode'] is not None else '-'
            }
            Repair Сoverage: {data['repair_coverage'] if data['repair_coverage'] else '-'}
            Демонстрационный: {
                status_to_word[data['demo_unit']] \
                    if data['demo_unit'] is not None else '-'
            }
            Восстановлен: {
                status_to_word[data['refurbished']] \
                    if data['refurbished'] is not None else '-'
            }
            Блокировка в США: {
                data['usa_block_status'] if data['usa_block_status'] else '-'
            }
            Сеть: {data['network'] if data['network'] else '-'}
        """
        answer_msg = re.sub(r"  ", "", answer_msg)
        
        if data['image']:
            await msg.answer_photo(photo=data['image'], caption=answer_msg)
        else:
            await msg.answer(answer_msg, parse_mode=None)