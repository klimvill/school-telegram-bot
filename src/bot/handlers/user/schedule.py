from datetime import datetime, timedelta

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.db.methods import get_schedule_day, add_extra_lesson
from src.bot.keybords import today_schedule_btn, paging_btn, add_extra_lesson_btn
from src.bot.misc import AddExtraLesson, create_schedule, create_short_schedule, create_extra_lesson
from src.resources.application_texts import add_extra_lesson_text

router_schedule = Router()


@router_schedule.message(Command('today'))
async def today(message: Message):
	"""Вывод расписания на текущий день"""
	today_date = datetime.today()
	date = today_date.strftime('%d %b. %Y г.')
	user_schedule_day = get_schedule_day(message.from_user.id, str(today_date.weekday()))

	text_message = create_schedule(date, user_schedule_day)
	text_message += '\n\n👇 Вы также можете посмотреть расписание на завтра'

	await message.answer(text_message, reply_markup=paging_btn)


@router_schedule.message(Command('tomorrow'))
async def tomorrow(message: Message):
	"""Вывод расписания на завтрашний день"""
	tomorrow_date = datetime.today() + timedelta(days=1)
	date = tomorrow_date.strftime('%d %b. %Y г.')
	user_schedule_day = get_schedule_day(message.from_user.id, str(tomorrow_date.weekday()))

	text_message = create_short_schedule(date, user_schedule_day)
	text_message += '\n\n👇 Вы также можете посмотреть расписание на сегодня'

	await message.answer(text_message, reply_markup=today_schedule_btn)


@router_schedule.message(Command('extraLesson'))
async def extra_lesson(message: Message):
	await message.answer(create_extra_lesson(message.from_user.id), reply_markup=today_schedule_btn)


@router_schedule.message(Command('addExtraLesson'))
async def add_extra_lesson_one(message: Message, state: FSMContext):
	await message.answer(add_extra_lesson_text, reply_markup=add_extra_lesson_btn)
	await state.set_state(AddExtraLesson.extra_lesson)


@router_schedule.message(AddExtraLesson.extra_lesson)
async def add_extra_lesson_two(message: Message, state: FSMContext):
	await state.update_data(extra_lesson=message.text)
	data = await state.get_data()
	await message.answer(add_extra_lesson(message.from_user.id, data['extra_lesson']))
	await state.clear()


# todo: Переписать
def check_message(message: Message, s) -> bool:
	return message.text is not None and message.text.lower() in s


@router_schedule.message(lambda message: check_message(message, ('пн', 'понедельник', 'monday', 'mon')))
async def monday(message: Message):
	user_schedule_day = get_schedule_day(message.from_user.id, '0')
	await message.answer(create_short_schedule('понедельник', user_schedule_day))


@router_schedule.message(lambda message: check_message(message, ('вт', 'вторник', 'tuesday', 'tue')))
async def tuesday(message: Message):
	user_schedule_day = get_schedule_day(message.from_user.id, '1')
	await message.answer(create_short_schedule('вторник', user_schedule_day))


@router_schedule.message(lambda message: check_message(message, ('ср', 'среда', 'wednesday', 'wed')))
async def wednesday(message: Message):
	user_schedule_day = get_schedule_day(message.from_user.id, '2')
	await message.answer(create_short_schedule('среду', user_schedule_day))


@router_schedule.message(lambda message: check_message(message, ('чт', 'четверг', 'thursday', 'thu')))
async def thursday(message: Message):
	user_schedule_day = get_schedule_day(message.from_user.id, '3')
	await message.answer(create_short_schedule('четверг', user_schedule_day))


@router_schedule.message(lambda message: check_message(message, ('пт', 'пятница', 'friday', 'fri')))
async def friday(message: Message):
	user_schedule_day = get_schedule_day(message.from_user.id, '4')
	await message.answer(create_short_schedule('пятницу', user_schedule_day))


@router_schedule.message(lambda message: check_message(message, ('сб', 'суббота', 'saturday', 'sat')))
async def saturday(message: Message):
	user_schedule_day = get_schedule_day(message.from_user.id, '5')
	await message.answer(create_short_schedule('субботу', user_schedule_day))


@router_schedule.message(lambda message: check_message(message, ('вс', 'воскресенье', 'sunday', 'sun')))
async def sunday(message: Message):
	user_schedule_day = get_schedule_day(message.from_user.id, '6')
	await message.answer(create_short_schedule('воскресенье', user_schedule_day))
