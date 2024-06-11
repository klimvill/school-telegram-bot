from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.database import get_schedule_day, reading_schedule, set_class, get_info_student, delete_extra_lesson
from bot.keybords import paging_btn, tomorrow_schedule_btn, yesterday_schedule_btn, teachers_btn_two, teachers_btn_one, \
	account_btn
from bot.misc import create_schedule, create_short_schedule, teachers_text, teachers_text_2, register_text, \
	delete_extra_lesson_text
from bot.state import ChangeClass

router_callback = Router()


@router_callback.callback_query(F.data == 'today')
async def today_callback(callback: CallbackQuery):
	"""Вывод расписания на текущий день"""
	today_date = datetime.today()
	date = today_date.today().strftime('%d %b. %Y г.')
	user_schedule_day = get_schedule_day(callback.from_user.id, str(today_date.weekday()))

	text_message = create_schedule(date, user_schedule_day)
	text_message += '\n\n👇 Вы также можете посмотреть расписание на завтра.'

	await callback.message.edit_text(text_message, reply_markup=paging_btn)


@router_callback.callback_query(F.data[:8] == 'tomorrow')
async def tomorrow_callback(callback: CallbackQuery):
	today_date = datetime.today()

	day = int(callback.data[8:])
	tomorrow_date = today_date + timedelta(days=day)
	date = tomorrow_date.strftime('%d %b. %Y г.')

	user_schedule_day = get_schedule_day(callback.from_user.id, str(tomorrow_date.weekday()))

	text_message = create_short_schedule(date, user_schedule_day)
	text_message += "\n\n👇 Вы также можете посмотреть расписание на сегодня."

	await callback.message.edit_text(text_message, reply_markup=await tomorrow_schedule_btn(day))


@router_callback.callback_query(F.data[:9] == 'yesterday')
async def yesterday_callback(callback: CallbackQuery):
	today_date = datetime.today()

	day = int(callback.data[9:])
	yesterday_date = today_date + timedelta(days=day)
	date = yesterday_date.strftime('%d %b. %Y г.')

	user_schedule_day = get_schedule_day(callback.from_user.id, str(yesterday_date.weekday()))

	text_message = create_short_schedule(date, user_schedule_day)
	text_message += "\n\n👇 Вы также можете посмотреть расписание на сегодня."

	await callback.message.edit_text(text_message, reply_markup=await yesterday_schedule_btn(day))


@router_callback.callback_query(F.data == 'delete_extra_lesson')
async def delete_extra_lesson_callback(callback: CallbackQuery, state: FSMContext):
	delete_extra_lesson(callback.from_user.id)
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
	await callback.message.edit_text(register_text)
	await state.set_state(ChangeClass.class_number)


@router_callback.message(ChangeClass.class_number)
async def change_class_callback_two(message: Message, state: FSMContext):
	if message.text.lower() in reading_schedule().keys():
		await state.update_data(class_number=message.text.lower())

		data = await state.get_data()
		set_class(message.from_user.id, data['class_number'])

		await state.clear()
		await message.answer('Вы успешно сменили класс!')

		info_student = get_info_student(message.from_user.id)

		text_message = (f'📔 ID: {info_student[0]}\n\n'
						f'🎭 Роль: {info_student[1]}\n\n'
						f'🌀 Класс: {info_student[2]}\n\n'
						f'📆 Дата регистрации: {info_student[3]}')

		await message.answer(text_message, reply_markup=account_btn)
	else:
		await message.answer('Вы ввели неверные данные. Попробуйте ещё раз.')


@router_callback.callback_query(F.data == 'change_role')
async def change_class_callback_one(callback: CallbackQuery):
	await callback.message.edit_text('Сменить роль')


@router_callback.callback_query(F.data == 'progress')
async def change_class_callback_one(callback: CallbackQuery):
	await callback.message.edit_text('Достижения')
