from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.database import get_info_student
from bot.keybords import teachers_btn_one, account_btn
from bot.misc import teachers_text

router_other = Router()


@router_other.message(Command('account'))
async def account(message: Message):
	info_student = get_info_student(message.from_user.id)

	text_message = (f'📔 ID: {info_student[0]}\n\n'
					f'🎭 Роль: {info_student[1]}\n\n'
					f'🌀 Класс: {info_student[2]}\n\n'
					f'📆 Дата регистрации: {info_student[3]}')

	await message.answer(text_message, reply_markup=account_btn)


@router_other.message(Command('teachers'))
async def teachers(message: Message):
	await message.answer(teachers_text, reply_markup=teachers_btn_one)


@router_other.message(Command('person'))
async def person(message: Message):
	pass


@router_other.message(Command('links'))
async def links(message: Message):
	pass
