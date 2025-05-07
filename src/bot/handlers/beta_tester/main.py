from aiogram import Dispatcher

from .test_function import router_test_function


def register_beta_tester_handlers(dp: Dispatcher):
    dp.include_router(router_test_function)
