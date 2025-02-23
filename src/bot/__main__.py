import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from handlers import register_all_handlers
from src.resources.application import BOT_TOKEN
from db import register_models


async def main():
	bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
	dp = Dispatcher()

	register_all_handlers(dp)
	register_models()
	await dp.start_polling(bot)


if __name__ == "__main__":
	# Пользуемся только при дебагинге на проде выключаем, будет медленно работать
	# logging.basicConfig(level=logging.INFO)

	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print('Exit')
