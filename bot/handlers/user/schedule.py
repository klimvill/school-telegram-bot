from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router_schedule = Router()


@router_schedule.message(Command('today'))
async def get_today_schedule(message: Message):
	await message.answer('Получение расписания на сегодняшний день.')


@router_schedule.message(Command('tomorrow'))
async def get_today_schedule(message: Message):
	await message.answer('Получение расписания на завтрашний день.')

