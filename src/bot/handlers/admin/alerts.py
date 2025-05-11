"""Обработка оповещений"""
import asyncio
from typing import Final

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot.db.methods import get_all_user
from src.bot.filters import IsAdmin
from src.bot.keybords import send_btn, send_back_btn
from src.bot.keybords.inline import generate_confirm_btn
from src.bot.misc import SendAllMessage
from src.resources.application_texts import (
	send_info_text, send_all_info_text
)

router_alerts = Router()


@router_alerts.message(Command('send'), IsAdmin())
async def send(message: Message):
	await message.answer(send_info_text, reply_markup=send_btn)


@router_alerts.callback_query(F.data == "all", IsAdmin())
async def send_all_callback_1(callback: CallbackQuery, state: FSMContext):
	await callback.message.edit_text(send_all_info_text, reply_markup=send_back_btn)
	await state.set_state(SendAllMessage.message)


@router_alerts.message(SendAllMessage.message, IsAdmin())
async def send_all_callback_2(message: Message, state: FSMContext):
	"""
	EFFECT_IDS: Final[dict[str: str]] = {
		"🔥": "5104841245755180586",
		"👍": "5107584321108051014",
		"🎉": "5046509860389126442",
		"👎": "5046509860389126442",
		"💩": "5046509860389126442",
	}

	message_effect = None

	if message.text is not None:
		for effect in ("🔥", "👍", "❤️", "🎉", "👎", "💩"):
			if message.text.endswith(effect):
				message_effect = EFFECT_IDS[effect]
	elif message.caption is not None:
		for effect in ("🔥", "👍", "❤️", "🎉", "👎", "💩"):
			if message.caption.endswith(effect):
				message_effect = EFFECT_IDS[effect]
	"""

	await message.send_copy(message.chat.id, reply_markup=await generate_confirm_btn("all"),
							message_effect_id="5159385139981059251")
	await state.clear()


@router_alerts.callback_query(F.data == "confirm_send:all")
async def send_all_callback_3(callback: CallbackQuery):
	good_send, bad_send = 0, 0
	users_id = [user.telegram_id for user in get_all_user()]

	copy_callback_message = await callback.message.delete_reply_markup()
	info_message = await callback.message.answer(f"Начинаю рассылку на {len(users_id)} пользователей...")

	for user_id in users_id:
		try:
			await copy_callback_message.send_copy(user_id)
			good_send += 1
		except Exception as e:
			bad_send += 1
			print(f"Ошибка при рассылке для {user_id}: {e}")
		finally:
			if good_send % 5 == 0:
				await info_message.edit_text(f"Рассылка: {good_send}/{len(users_id)} отправлено, {bad_send} ошибок")
			await asyncio.sleep(0.05)

	await info_message.edit_text(f"Рассылка завершена!\nУспешно: {good_send}\nНе удалось: {bad_send}")


@router_alerts.callback_query(F.data == "one", IsAdmin())
async def send_one_callback(callback: CallbackQuery):
	await callback.message.edit_text("one", reply_markup=send_back_btn)


@router_alerts.callback_query(F.data == "send_back", IsAdmin())
async def send_one_callback(callback: CallbackQuery, state: FSMContext):
	await callback.message.edit_text(send_info_text, reply_markup=send_btn)
	await state.clear()
