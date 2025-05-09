"""Обработка оповещений"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
import asyncio
from src.bot.filters import IsAdmin
from src.bot.keybords import send_btn, send_back_btn
from src.bot.misc import SendAllMessage
from src.bot.db.methods import get_all_user
from src.resources.application_texts import (
	send_info_text, send_all_info_text
)

router_alerts = Router()


@router_alerts.message(Command('send'), IsAdmin())
async def send(message: Message):
	await message.answer(send_info_text, reply_markup=send_btn)


@router_alerts.callback_query(F.data == "all")
async def send_all_callback_1(callback: CallbackQuery, state: FSMContext):
	await callback.message.edit_text(send_all_info_text, reply_markup=send_back_btn)
	await state.set_state(SendAllMessage.message)


@router_alerts.message(SendAllMessage.message)
async def send_all_callback_2(message: Message, state: FSMContext):
	# todo: Сделать подтверждение рассылки
	"""
	@dp.message(lambda message: is_admin(message.from_user.id) and message.reply_to_message is None)
	async def handle_broadcast_message(message: types.Message):
		if message.text and (message.text.startswith('/') or message.text in ["Рассылка", "Статистика"]):
			return

		confirm_kb = types.InlineKeyboardMarkup(inline_keyboard=[
			[types.InlineKeyboardButton(text="Начать рассылку", callback_data=f"confirm_broadcast:{message.message_id}")],
			[types.InlineKeyboardButton(text="Отмена", callback_data="cancel_broadcast")]
		])

		if message.text:
			preview = message.text[:100] + "..." if len(message.text) > 100 else message.text
			await message.reply(f"Подтвердите рассылку этого сообщения:\n\n{preview}", reply_markup=confirm_kb)
		elif message.caption:
			preview = message.caption[:100] + "..." if len(message.caption) > 100 else message.caption
			media_type = "фото" if message.photo else "видео" if message.video else "документ"
			await message.reply(f"Подтвердите рассылку {media_type} с подписью:\n\n{preview}", reply_markup=confirm_kb)
		else:
			media_type = "фото" if message.photo else "видео" if message.video else "документ"
			await message.reply(f"Подтвердите рассылку {media_type} без подписи", reply_markup=confirm_kb)
	"""

	await state.clear()

	good_send, bad_send = 0, 0
	users_id = [user.telegram_id for user in get_all_user()]

	info_message = await message.answer(f"Начинаю рассылку на {len(users_id)} пользователей...")
	bot = message.bot

	for user_id in users_id:
		try:
			# Копируем оригинальное сообщение
			if message.text and not message.photo and not message.video and not message.document:
				# Просто текст
				await bot.send_message(user_id, message.text, entities=message.entities)
			elif message.photo:
				# Фото с подписью или без
				await bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption,
									 caption_entities=message.caption_entities)
			elif message.video:
				# Видео с подписью или без
				await bot.send_video(user_id, message.video.file_id, caption=message.caption,
									 caption_entities=message.caption_entities)
			elif message.document:
				# Документ с подписью или без
				await bot.send_document(user_id, message.document.file_id, caption=message.caption,
										caption_entities=message.caption_entities)
			else:
				# Другие типы сообщений можно добавить по аналогии
				await bot.copy_message(user_id, message.chat.id, message.message_id)

			good_send += 1
			if good_send % 10 == 0:
				await info_message.edit_text(f"Рассылка: {good_send}/{len(users_id)} отправлено, {bad_send} ошибок")
		except Exception as e:
			bad_send += 1
		finally:
			# Задержка для соблюдения лимитов Telegram (30 сообщений в секунду)
			await asyncio.sleep(0.05)

	await info_message.edit_text(f"Рассылка завершена!\nУспешно: {good_send}\nНе удалось: {bad_send}")


@router_alerts.callback_query(F.data == "one")
async def send_one_callback(callback: CallbackQuery):
	await callback.message.edit_text("one", reply_markup=send_back_btn)


@router_alerts.callback_query(F.data == "send_back")
async def send_one_callback(callback: CallbackQuery, state: FSMContext):
	await callback.message.edit_text(send_info_text, reply_markup=send_btn)
	await state.clear()
