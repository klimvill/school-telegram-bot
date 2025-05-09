from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

today_schedule_btn = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='📆 Расписание на сегодня', callback_data='today')],
])
paging_btn = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='◀️ Назад', callback_data='slider:-1'),
	 InlineKeyboardButton(text='Вперед ▶️', callback_data='slider:1')],
])
teachers_btn_one = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='Вперед ▶️', callback_data='teachers_two_sheet')],
])
teachers_btn_two = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='◀️ Назад', callback_data='teachers_one_sheet')],
])
add_extra_lesson_btn = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text="🗑 Удалить", callback_data="delete_extra_lesson")],
	[InlineKeyboardButton(text="◀️ Выйти", callback_data="exit_add_extra_lesson")],
])
account_btn = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text="🌀 Сменить класс", callback_data="change_class")],
	[InlineKeyboardButton(text="🎭 Сменить роль", callback_data="change_role")],
	[InlineKeyboardButton(text="🌟 Достижения", callback_data="progress")],
])
account_back_btn = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='◀️ Назад', callback_data='account_back')],
])

send_btn = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text="📣 Всем", callback_data="all")],
	[InlineKeyboardButton(text="💬 Классу", callback_data="one")]
])
send_back_btn = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='◀️ Назад', callback_data='send_back')],
])


async def schedule_btn(day: int):
	keyboard = InlineKeyboardBuilder()
	tomorrow_callback = f'slider:{day + 1}'
	yesterday_callback = f'slider:{day - 1}'

	if day == -1:
		tomorrow_callback = 'today'
	elif day == 1:
		yesterday_callback = 'today'

	btn_tomorrow = InlineKeyboardButton(text="Вперед ▶️", callback_data=tomorrow_callback)
	btn_yesterday = InlineKeyboardButton(text="◀️ Назад", callback_data=yesterday_callback)

	keyboard.add(InlineKeyboardButton(text="📆 Расписание на сегодня", callback_data="today"))
	keyboard.row(btn_yesterday, btn_tomorrow)

	return keyboard.as_markup()
