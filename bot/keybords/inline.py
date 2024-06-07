from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

today_schedule_btn = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='📆 Расписание на сегодня', callback_data='today')],
])
paging_btn = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='◀️ Назад', callback_data='tomorrow1'),
	 InlineKeyboardButton(text='Вперед ▶️', callback_data='yesterday-1')],
])
