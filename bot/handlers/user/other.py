from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.keybords import teachers_btn_one
from bot.misc import teachers_text

router_other = Router()


@router_other.message(Command('account'))
async def account(message: Message):
	pass


@router_other.message(Command('teachers'))
async def teachers(message: Message):
	await message.answer(teachers_text, reply_markup=teachers_btn_one)


@router_other.message(Command('person'))
async def person(message: Message):
	pass


@router_other.message(Command('links'))
async def links(message: Message):
	pass
