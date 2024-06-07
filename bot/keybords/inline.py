from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

today_schedule_btn = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='📆 Расписание на сегодня', callback_data='today')],
])
