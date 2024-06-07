import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from .handlers import router
from .misc import BOT_TOKEN


async def main():
	bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
	db = Dispatcher()

	db.include_router(router)
	await db.start_polling(bot)


def start_bot():
	# Пользуемся только при дебагинге на проде выключаем, будет медленно работать
	logging.basicConfig(level=logging.INFO)

	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print('Exit')
