from aiogram.fsm.state import StatesGroup, State


class Register(StatesGroup):
	class_number: str = State()


class AddExtraLesson(StatesGroup):
	extra_lesson: str = State()


class ChangeClass(StatesGroup):
	class_number: str = State()
