from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.db.enums import RoleType
from src.bot.db.methods import check_if_user_exists, add_new_user, schedule
from src.bot.keybords import today_schedule_btn
from src.resources.application_texts import start_text, register_text, help_text, calls_text, forms_text
from src.bot.misc import Register

router_basic_cmd = Router()


@router_basic_cmd.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
	await message.answer(start_text)

	if not check_if_user_exists(message.from_user.id):
		await message.answer(forms_text, disable_web_page_preview=True)
		await message.answer(register_text)
		await state.set_state(Register.class_number)


@router_basic_cmd.message(Command('help'))
async def get_help(message: Message):
	await message.answer(help_text, disable_web_page_preview=True)


@router_basic_cmd.message(Command('calls'))
async def calls(message: Message):
	await message.answer(calls_text, reply_markup=today_schedule_btn)


@router_basic_cmd.message(Register.class_number)
async def register_user(message: Message, state: FSMContext):
	if message.text.lower() in schedule.keys():
		await state.update_data(class_number=message.text.lower())

		data = await state.get_data()
		add_new_user(message.from_user.id, message.from_user.username, RoleType.USER, data['class_number'])

		await state.clear()
		await message.answer('Вы успешно зарегистрировались!')
	else:
		await message.answer('Вы ввели неверные данные. Попробуйте ввести номер и букву класса ещё раз.')
