from aiogram import Dispatcher

from .basic_cmd import router_basic_cmd
from .schedule import router_schedule
from .other import router_other


def register_user_handlers(dp: Dispatcher):
	for router in (router_basic_cmd, router_schedule, router_other):
		dp.include_router(router)
