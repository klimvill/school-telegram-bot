from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

today_schedule_btn = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='📆 Расписание на сегодня', callback_data='today')],
])
paging_btn = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='◀️ Назад', callback_data='tomorrow-1'),
	 InlineKeyboardButton(text='Вперед ▶️', callback_data='yesterday1')],
])
teachers_btn_one = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='Вперед ▶️', callback_data='teachers_two_sheet')],
])
teachers_btn_two = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='◀️ Назад', callback_data='teachers_one_sheet')],
])
add_extra_lesson_btn = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text="🗑 Удалить", callback_data="delete_schedule")],
	[InlineKeyboardButton(text="◀️ Назад", callback_data="exit_add_extra_lesson")],
])


async def tomorrow_schedule_btn(day: int):
	keyboard = InlineKeyboardBuilder()

	btn_tomorrow = InlineKeyboardButton(text="Вперед ▶️", callback_data=f"tomorrow{day + 1}")
	if day + 1 == 0:
		btn_tomorrow = InlineKeyboardButton(text="Вперед ▶️", callback_data=f"today")

	btn_yesterday = InlineKeyboardButton(text="◀️ Назад", callback_data=f"yesterday{day - 1}")
	if day - 1 == 0:
		btn_yesterday = InlineKeyboardButton(text="◀️ Назад", callback_data="today")

	keyboard.add(InlineKeyboardButton(text="📆 Расписание на сегодня", callback_data="today"))
	keyboard.row(btn_yesterday, btn_tomorrow)

	return keyboard.as_markup()


async def yesterday_schedule_btn(day: int):
	keyboard = InlineKeyboardBuilder()

	btn_tomorrow = InlineKeyboardButton(text="Вперед ▶️", callback_data=f"tomorrow{day + 1}")
	if day + 1 == 0:
		btn_tomorrow = InlineKeyboardButton(text="Вперед ▶️", callback_data=f"today")

	btn_yesterday = InlineKeyboardButton(text="◀️ Назад", callback_data=f"yesterday{day - 1}")
	if day - 1 == 0:
		btn_yesterday = InlineKeyboardButton(text="◀️ Назад", callback_data="today")

	keyboard.add(InlineKeyboardButton(text="📆 Расписание на сегодня", callback_data="today"))
	keyboard.row(btn_yesterday, btn_tomorrow)

	return keyboard.as_markup()
