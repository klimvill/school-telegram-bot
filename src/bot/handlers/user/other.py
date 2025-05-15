from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from src.bot.db.methods import get_info_user, get_photo_path
from src.bot.keybords import teachers_btn_one, account_btn
from src.resources.application_texts import teachers_text, links_text, person_text

router_other = Router()


@router_other.message(Command('account'))
async def account(message: Message):
	info_student = get_info_user(message.from_user.id)

	text_message = (f'📔 ID: {info_student[0]}\n\n'
					f'🎭 Роль: {info_student[1].value}\n\n'
					f'🌀 Класс: {info_student[2]}\n\n'
					f"📆 Дата регистрации: {info_student[3].strftime('%d %b. %Y')}")

	photo_file = FSInputFile(path=await get_photo_path(message.from_user.id))
	await message.answer_photo(photo_file, caption=text_message, reply_markup=account_btn)


@router_other.message(Command('teachers'))
async def teachers(message: Message):
	await message.answer(teachers_text, reply_markup=teachers_btn_one)


@router_other.message(Command('person'))
async def person(message: Message):
	await message.answer(person_text)


@router_other.message(Command('links'))
async def links(message: Message):
	await message.answer(links_text)
