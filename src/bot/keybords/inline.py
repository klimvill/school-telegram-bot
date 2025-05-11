from typing import Literal

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
	[
		InlineKeyboardButton(text="👍", callback_data="send_effect:like"),
		InlineKeyboardButton(text="🔥", callback_data="send_effect:fire"),
		InlineKeyboardButton(text="🎉", callback_data="send_effect:"),
		InlineKeyboardButton(text="✅ ❤️", callback_data="send_effect:"),
		InlineKeyboardButton(text="👎", callback_data="send_effect:"),
	],
	[InlineKeyboardButton(text='◀️ Назад', callback_data='send_back')],
])
confirm_btn = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text="✅ Начать рассылку", callback_data="confirm_send")],
	[InlineKeyboardButton(text="❌ Отмена", callback_data="cansel_send")]
])


async def generate_confirm_btn(send_type: Literal["all", "one"]) -> InlineKeyboardMarkup:
	return InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text="✅ Начать рассылку", callback_data=f"confirm_send:{send_type}")],
		[InlineKeyboardButton(text="❌ Отмена", callback_data=f"cansel_send")]
	])


async def generate_schedule_btn(day: int) -> InlineKeyboardMarkup:
	keyboard = InlineKeyboardBuilder()
	tomorrow_callback = f'slider:{day + 1}' if day != -1 else 'today'
	yesterday_callback = f'slider:{day - 1}' if day != 1 else 'today'

	btn_tomorrow = InlineKeyboardButton(text="Вперед ▶️", callback_data=tomorrow_callback)
	btn_yesterday = InlineKeyboardButton(text="◀️ Назад", callback_data=yesterday_callback)

	keyboard.add(InlineKeyboardButton(text="📆 Расписание на сегодня", callback_data="today"))
	keyboard.row(btn_yesterday, btn_tomorrow)

	return keyboard.as_markup()
