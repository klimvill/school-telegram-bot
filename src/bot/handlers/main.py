from aiogram import Dispatcher

from .admin.main import register_admin_handlers
from .beta_tester.main import register_beta_tester_handlers
from .user.main import register_user_handlers


def register_all_handlers(dp: Dispatcher):
	register_admin_handlers(dp)
	register_beta_tester_handlers(dp)
	register_user_handlers(dp)
