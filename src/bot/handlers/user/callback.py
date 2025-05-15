from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from src.bot.db.methods import get_schedule_day, schedule, set_class, get_info_user, delete_extra_lessons, \
	get_photo_path
from src.bot.keybords import paging_btn, generate_schedule_btn, teachers_btn_two, teachers_btn_one, account_btn, \
	account_back_btn
from src.bot.misc import create_schedule, create_short_schedule, ChangeClass
from src.resources.application_texts import teachers_text, teachers_text_2, register_text, delete_extra_lesson_text

router_callback = Router()


@router_callback.callback_query(F.data == 'today')
async def today_callback(callback: CallbackQuery):
	"""Вывод расписания на текущий день"""
	today_date = datetime.today()
	date = today_date.today().strftime('%d %b. %Y г.')
	user_schedule_day = get_schedule_day(callback.from_user.id, str(today_date.weekday()))

	text_message = create_schedule(date, user_schedule_day)
	text_message += '\n\n👇 Вы также можете посмотреть расписание на завтра'

	await callback.message.edit_text(text_message, reply_markup=paging_btn)


@router_callback.callback_query(F.data[:6] == 'slider')
async def slider_callback(callback: CallbackQuery):
	today_date = datetime.today()

	day = int(callback.data[7:])
	tomorrow_date = today_date + timedelta(days=day)
	date = tomorrow_date.strftime('%d %b. %Y г.')

	user_schedule_day = get_schedule_day(callback.from_user.id, str(tomorrow_date.weekday()))

	text_message = create_short_schedule(date, user_schedule_day)
	text_message += "\n\n👇 Вы также можете посмотреть расписание на сегодня"

	await callback.message.edit_text(text_message, reply_markup=await generate_schedule_btn(day))


@router_callback.callback_query(F.data == 'delete_extra_lesson')
async def delete_extra_lesson_callback(callback: CallbackQuery, state: FSMContext):
	delete_extra_lessons(callback.from_user.id)
	await state.clear()
	await callback.message.edit_text(delete_extra_lesson_text)


@router_callback.callback_query(F.data == 'exit_add_extra_lesson')
async def exit_extra_lesson_callback(callback: CallbackQuery, state: FSMContext):
	await state.clear()
	await callback.message.edit_text('Вы вышли из режима добавления расписания')


@router_callback.callback_query(F.data == 'teachers_two_sheet')
async def teachers_one_sheet_callback(callback: CallbackQuery):
	await callback.message.edit_text(teachers_text_2, reply_markup=teachers_btn_two)


@router_callback.callback_query(F.data == 'teachers_one_sheet')
async def teachers_one_sheet_callback(callback: CallbackQuery):
	await callback.message.edit_text(teachers_text, reply_markup=teachers_btn_one)


@router_callback.callback_query(F.data == 'change_class')
async def change_class_callback_one(callback: CallbackQuery, state: FSMContext):
	await callback.message.delete()
	await callback.message.answer(register_text)
	await state.set_state(ChangeClass.class_number)


@router_callback.message(ChangeClass.class_number)
async def change_class_callback_two(message: Message, state: FSMContext):
	if message.text.lower() in schedule.keys():
		set_class(message.from_user.id, message.text.lower())

		await state.clear()
		await message.answer('Вы успешно сменили класс!')

		info_student = get_info_user(message.from_user.id)

		text_message = (f'📔 ID: {info_student[0]}\n\n'
						f'🎭 Роль: {info_student[1].value}\n\n'
						f'🌀 Класс: {info_student[2]}\n\n'
						f"📆 Дата регистрации: {info_student[3].strftime('%d %b. %Y')}")

		photo_file = FSInputFile(path=await get_photo_path(message.from_user.id))
		await message.answer_photo(photo_file, caption=text_message, reply_markup=account_btn)
	else:
		await message.answer('Вы ввели неверные данные. Попробуйте ещё раз.')


@router_callback.callback_query(F.data == 'change_role')
async def change_class_callback_one(callback: CallbackQuery):
	await callback.message.delete()
	await callback.message.answer('Чтобы изменить роль пишите @klimvill', reply_markup=account_back_btn)


@router_callback.callback_query(F.data == 'progress')
async def change_class_callback_one(callback: CallbackQuery):
	await callback.message.delete()
	await callback.message.answer('Достижения', reply_markup=account_back_btn)


@router_callback.callback_query(F.data == 'account_back')
async def teachers_one_sheet_callback(callback: CallbackQuery):
	info_student = get_info_user(callback.from_user.id)

	text_message = (f'📔 ID: {info_student[0]}\n\n'
					f'🎭 Роль: {info_student[1].value}\n\n'
					f'🌀 Класс: {info_student[2]}\n\n'
					f"📆 Дата регистрации: {info_student[3].strftime('%d %b. %Y')}")

	await callback.message.delete()
	photo_file = FSInputFile(path=await get_photo_path(callback.from_user.id))
	await callback.message.answer_photo(photo_file, caption=text_message, reply_markup=account_btn)

