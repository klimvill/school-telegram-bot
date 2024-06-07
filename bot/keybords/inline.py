from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

today_schedule_btn = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='📆 Расписание на сегодня', callback_data='today')],
])
paging_btn = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='◀️ Назад', callback_data='tomorrow1'),
	 InlineKeyboardButton(text='Вперед ▶️', callback_data='yesterday-1')],
])
teachers_btn_one = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='Вперед ▶️', callback_data='teachers_two_sheet')],
])
add_extra_lesson_btn = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text="🗑 Удалить", callback_data="delete_schedule")],
	[InlineKeyboardButton(text="◀️ Назад", callback_data="exit_add_extra_lesson")],
])
