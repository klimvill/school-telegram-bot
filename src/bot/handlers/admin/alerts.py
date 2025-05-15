"""Обработка оповещений"""
import asyncio

from aiogram import Router, F
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot.db.methods import get_all_user
from src.bot.filters import IsAdmin
from src.bot.keybords import send_btn, generate_reactions_back_btn
from src.bot.keybords.inline import generate_confirm_btn
from src.bot.misc import SendAllMessage
from src.resources.application import EFFECT_IDS
from src.resources.application_texts import (
	send_info_text, send_all_info_text, send_during_text, send_end_text
)

router_alerts = Router()


@router_alerts.message(Command('send'), IsAdmin())
async def send(message: Message):
	await message.answer(send_info_text, reply_markup=send_btn)


@router_alerts.callback_query(F.data == "all", IsAdmin())
async def send_all_callback_1(callback: CallbackQuery, state: FSMContext):
	await state.update_data(effect=None)

	await callback.message.edit_text(send_all_info_text, reply_markup=await generate_reactions_back_btn(None))
	await state.set_state(SendAllMessage.message)


@router_alerts.callback_query(F.data.startswith("send_effect:"))
async def send_effect_callback(callback: CallbackQuery, state: FSMContext):
	old_effect = (await state.get_data())['effect']
	effect = callback.data.split(":")[1]
	effect = effect if effect != old_effect else None

	await state.update_data(effect=effect)
	await callback.message.edit_reply_markup(reply_markup=await generate_reactions_back_btn(effect))


@router_alerts.message(SendAllMessage.message, IsAdmin())
async def send_all_callback_2(message: Message, state: FSMContext):
	effect = (await state.get_data())['effect']
	effect_id = EFFECT_IDS[effect] if effect is not None else None

	await message.send_copy(
		message.chat.id, message_effect_id=effect_id,
		reply_markup=await generate_confirm_btn("all")
	)


@router_alerts.callback_query(F.data == "confirm_send:all")
async def send_all_callback_3(callback: CallbackQuery):
	good_send, bad_send, blocked_bot = 0, 0, 0
	users_id = [user.telegram_id for user in get_all_user()]

	copy_callback_message = await callback.message.delete_reply_markup()
	await callback.message.delete()
	info_message = await callback.message.answer(
		send_during_text.format(len(users_id), good_send, bad_send, blocked_bot)
	)

	for user_id in users_id:
		try:
			await copy_callback_message.send_copy(user_id)
			good_send += 1
		except TelegramForbiddenError:
			blocked_bot += 1
		except Exception as e:
			bad_send += 1
			print(f"Ошибка при рассылке для {user_id}: {e}")
		finally:
			if good_send % 5 == 0:
				await info_message.edit_text(send_during_text.format(len(users_id), good_send, bad_send, blocked_bot))
			await asyncio.sleep(0.05)

	await info_message.edit_text(send_end_text.format(len(users_id), good_send, bad_send, blocked_bot))


@router_alerts.callback_query(F.data == "cansel_send")
async def send_all_callback_3(callback: CallbackQuery):
	await callback.message.delete()


@router_alerts.callback_query(F.data == "one", IsAdmin())
async def send_one_callback(callback: CallbackQuery):
	await callback.message.edit_text("one", reply_markup=await generate_reactions_back_btn(None))


@router_alerts.callback_query(F.data == "send_back", IsAdmin())
async def send_one_callback(callback: CallbackQuery, state: FSMContext):
	await callback.message.edit_text(send_info_text, reply_markup=send_btn)
	await state.clear()
