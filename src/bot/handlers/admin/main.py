from aiogram import Dispatcher

from .alerts import router_alerts
from .refresh_schedule import router_refresh_schedule
from .user_management import router_user_management


def register_admin_handlers(dp: Dispatcher):
    dp.include_router(router_alerts)
    dp.include_router(router_refresh_schedule)
    dp.include_router(router_user_management)
