from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from ..misc import start_text, help_text

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
	await message.answer(start_text)


@router.message(Command('help'))
async def get_help(message: Message):
	await message.answer(help_text, disable_web_page_preview=True)
