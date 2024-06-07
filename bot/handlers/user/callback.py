from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.database import get_schedule_day
from bot.keybords import paging_btn, tomorrow_schedule_btn, yesterday_schedule_btn, teachers_btn_two, teachers_btn_one
from bot.misc import create_schedule, create_short_schedule, teachers_text, teachers_text_2

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


@router_callback.callback_query(F.data == 'teachers_two_sheet')
async def teachers_one_sheet_callback(callback: CallbackQuery):
	await callback.message.edit_text(teachers_text_2, reply_markup=teachers_btn_two)


@router_callback.callback_query(F.data == 'teachers_one_sheet')
async def teachers_one_sheet_callback(callback: CallbackQuery):
	await callback.message.edit_text(teachers_text, reply_markup=teachers_btn_one)
