import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.config import settings
from bot.dependecies.database import SessionLocal
from bot.handlers import router

from .cruds import user_crud


async def main():
    bot = Bot(token=settings.TELEGRAM_TOKEN)

    async with SessionLocal() as db:
        if not await user_crud.are_users_exists(db):
            await user_crud.add_user(db, settings.ADMIN_ID, level_permission=5)
    
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())