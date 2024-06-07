from aiogram.fsm.state import StatesGroup, State


class Register(StatesGroup):
	class_number: str = State()
