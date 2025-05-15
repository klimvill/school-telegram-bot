from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.db.enums import RoleType
from src.bot.db.methods import check_if_user_exists, add_new_user, schedule, add_photo
from src.bot.keybords import today_schedule_btn
from src.bot.misc import Register
from src.resources.application import ADMINS_ID, BETA_TESTERS_ID, TEACHERS
from src.resources.application_texts import (
	start_text, register_text, help_text, calls_text, forms_text,
	successful_registration_text, invalid_class_format_error,
	telegram_id_text, welcome_admin_text, welcome_beta_tester_text,
	welcome_teacher_text
)

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


@router_basic_cmd.message(Command('id'))
async def get_telegram_id(message: Message):
	await message.answer(telegram_id_text.format(message.from_user.id))


@router_basic_cmd.message(Register.class_number)
async def register_user_two(message: Message, state: FSMContext):
	if message.text.lower() in schedule.keys():
		await state.update_data(class_number=message.text.lower())

		# await state.clear()
		await state.set_state(Register.photo_profile)
		await message.answer("Пришлите фотографию для вашего профиля")

	else:
		await message.answer(invalid_class_format_error)


@router_basic_cmd.message(Register.photo_profile)
async def register_user_two(message: Message, state: FSMContext):
	if message.photo is None:
		await message.answer("Пришлите фотографию!")
	else:
		file_info = await message.bot.get_file(message.photo[-1].file_id)
		downloaded_file = await message.bot.download_file(file_info.file_path)
		await message.answer("Фото установленно!")

		role = RoleType.USER
		if message.from_user.id in ADMINS_ID:
			await message.answer(welcome_admin_text)
			role = RoleType.ADMIN
		elif str(message.from_user.id) in TEACHERS:
			await message.answer(welcome_teacher_text)
			role = RoleType.TEACHER
		elif message.from_user.id in BETA_TESTERS_ID:
			await message.answer(welcome_beta_tester_text)
			role = RoleType.BETA_TESTER
		data = await state.get_data()
		add_new_user(message.from_user.id, message.from_user.username, role, data["class_number"])
		await add_photo(message.from_user.id, downloaded_file)
		await message.answer(successful_registration_text)

		await state.clear()


@router_basic_cmd.message(Command('calls'))
async def calls(message: Message):
	# Эта функция должна находится ниже register_user, иначе может произойти баг.
	await message.answer(calls_text, reply_markup=today_schedule_btn)
