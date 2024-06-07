from datetime import datetime, timedelta

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.database import get_schedule_day
from bot.keybords import today_schedule_btn, paging_btn
from bot.misc import create_schedule, create_short_schedule

router_schedule = Router()


@router_schedule.message(Command('today'))
async def today(message: Message):
	"""Вывод расписания на текущий день"""
	today_date = datetime.today()
	date = today_date.today().strftime('%d %b. %Y г.')
	user_schedule_day = get_schedule_day(message.from_user.id, str(today_date.weekday()))

	text_message = create_schedule(date, user_schedule_day)
	text_message += '\n\n👇 Вы также можете посмотреть расписание на завтра.'

	await message.answer(text_message, reply_markup=paging_btn)


@router_schedule.message(Command('tomorrow'))
async def tomorrow(message: Message):
	"""Вывод расписания на завтрашний день"""
	tomorrow_date = datetime.today() + timedelta(days=1)
	date = tomorrow_date.today().strftime('%d %b. %Y г.')
	user_schedule_day = get_schedule_day(message.from_user.id, str(tomorrow_date.weekday()))

	text_message = create_schedule(date, user_schedule_day)
	text_message += '\n\n👇 Вы также можете посмотреть расписание на сегодня.'

	await message.answer(text_message, reply_markup=today_schedule_btn)


@router_schedule.message(Command('extraLesson'))
async def extra_lesson(message: Message):
	await message.answer('Расписание дополнительных занятий')


@router_schedule.message(Command('addExtraLesson'))
async def add_extra_lesson(message: Message):
	await message.answer('Добавление расписания дополнительных занятий')


# Если использовать F.text - выдаёт ошибку
@router_schedule.message(lambda message: message.text.lower() in ('пн', 'понедельник', 'monday', 'mon'))
async def monday(message: Message):
	user_schedule_day = get_schedule_day(message.from_user.id, '0')
	await message.answer(create_short_schedule('понедельник', user_schedule_day))


@router_schedule.message(lambda message: message.text.lower() in ('вт', 'вторник', 'tuesday', 'tue'))
async def tuesday(message: Message):
	user_schedule_day = get_schedule_day(message.from_user.id, '1')
	await message.answer(create_short_schedule('вторник', user_schedule_day))


@router_schedule.message(lambda message: message.text.lower() in ('ср', 'среда', 'wednesday', 'wed'))
async def wednesday(message: Message):
	user_schedule_day = get_schedule_day(message.from_user.id, '2')
	await message.answer(create_short_schedule('среда', user_schedule_day))


@router_schedule.message(lambda message: message.text.lower() in ('чт', 'четверг', 'thursday', 'thu'))
async def thursday(message: Message):
	user_schedule_day = get_schedule_day(message.from_user.id, '3')
	await message.answer(create_short_schedule('четверг', user_schedule_day))


@router_schedule.message(lambda message: message.text.lower() in ('пт', 'пятница', 'friday', 'fri'))
async def friday(message: Message):
	user_schedule_day = get_schedule_day(message.from_user.id, '4')
	await message.answer(create_short_schedule('пятница', user_schedule_day))


@router_schedule.message(lambda message: message.text.lower() in ('сб', 'суббота', 'saturday', 'sat'))
async def saturday(message: Message):
	user_schedule_day = get_schedule_day(message.from_user.id, '5')
	await message.answer(create_short_schedule('суббота', user_schedule_day))


@router_schedule.message(lambda message: message.text.lower() in ('вс', 'воскресенье', 'sunday', 'sun'))
async def sunday(message: Message):
	user_schedule_day = get_schedule_day(message.from_user.id, '6')
	await message.answer(create_short_schedule('воскресенье', user_schedule_day))
