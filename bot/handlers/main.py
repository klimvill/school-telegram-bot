from aiogram import Dispatcher

from .admin import register_admin_handlers
from .user import register_user_handlers


def register_all_handlers(dp: Dispatcher):
	register_admin_handlers(dp)
	register_user_handlers(dp)
