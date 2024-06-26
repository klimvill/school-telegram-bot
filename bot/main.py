import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from .handlers import register_all_handlers
from .config import BOT_TOKEN
from .database import register_db


async def main():
	bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
	dp = Dispatcher()

	register_all_handlers(dp)
	register_db()
	await dp.start_polling(bot)


def start_bot():
	# Пользуемся только при дебагинге на проде выключаем, будет медленно работать
	logging.basicConfig(level=logging.INFO)

	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print('Exit')
