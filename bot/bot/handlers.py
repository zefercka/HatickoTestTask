from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.services import start, login, imei, add, delete, list_s

from bot.config import settings

router = Router()


@router.message(Command("start"))
async def start_command(msg: Message):
    await start.start_command(msg)



@router.message(Command("login"))
async def login_command(msg: Message):
    await login.login_command(msg)
    

@router.message(Command("imei"))
async def imei_command(msg: Message):
    await imei.imei_command(msg)


@router.message(Command("add"))
async def add_command(msg: Message):
    await add.add_command(msg)


@router.message(Command("delete"))
async def delete_command(msg: Message):
    await delete.delete_command(msg)
    

@router.message(Command("list"))
async def list_command(msg: Message):
    await list_s.list_command(msg)