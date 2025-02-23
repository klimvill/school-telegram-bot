from enum import Enum, auto

CLASSES = ()  # Тут будет список всех классов


class RoleType(Enum):
	ADMIN = "Школьник-админ"
	USER = "Школьник"


class DaysOfWeek(Enum):
	MONDAY = auto()
	TUESDAY = auto()
	WEDNESDAY = auto()
	THURSDAY = auto()
	FRIDAY = auto()
	SATURDAY = auto()
	SUNDAY = auto()

	@staticmethod
	def to_string(day: "DaysOfWeek") -> str:
		return ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье')[day.value]

	@staticmethod
	def week_day(day: str) -> "DaysOfWeek":
		index = ('понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье').index(day.lower())
		return (DaysOfWeek.MONDAY, DaysOfWeek.THURSDAY, DaysOfWeek.WEDNESDAY, DaysOfWeek.THURSDAY,
				DaysOfWeek.FRIDAY, DaysOfWeek.SATURDAY, DaysOfWeek.SUNDAY)[index]


class SmileType(Enum):
	...
