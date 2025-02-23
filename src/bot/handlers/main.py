from aiogram import Dispatcher

from .user.main import register_user_handlers


def register_all_handlers(dp: Dispatcher):
	register_user_handlers(dp)
