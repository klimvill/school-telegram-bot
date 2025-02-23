from aiogram import Dispatcher

from .basic_cmd import router_basic_cmd
from .schedule import router_schedule
from .other import router_other
from .callback import router_callback


def register_user_handlers(dp: Dispatcher):
	for router in (router_basic_cmd, router_schedule, router_other, router_callback):
		dp.include_router(router)
