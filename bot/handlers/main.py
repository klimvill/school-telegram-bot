from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ..database import *
from ..misc import start_text, help_text
from ..state import *

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
	await message.answer(start_text)

	if not check_if_user_exists(message.from_user.id):
		await message.answer('Зарегистрируйтесь, написав в чат номер и букву класса.\n\nНапример: 9Г, 11а, 8В.')
		await state.set_state(Register.class_number)


@router.message(Command('help'))
async def get_help(message: Message):
	await message.answer(help_text, disable_web_page_preview=True)


@router.message(Register.class_number)
async def register_user_one(message: Message, state: FSMContext):
	if message.text.lower() in reading_schedule().keys():
		await state.update_data(class_number=message.text)

		data = await state.get_data()
		add_new_user(message.from_user.id, data)

		await state.clear()
		await message.answer('Вы успешно зарегистрировались!')
	else:
		await message.answer('Вы ввели неверные данные. Напишите ещё раз.')
