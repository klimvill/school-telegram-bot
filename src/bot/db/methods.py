from datetime import datetime
from locale import setlocale, LC_ALL
from typing import NoReturn, List, Tuple

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from .enums import RoleType, DaysOfWeek
from .main import reading_schedule, Database
from .models import User, ExtraLesson
from ...resources.application import IS_GOOGLE

setlocale(category=LC_ALL, locale="Russian")  # Настройка локализации для правильной работы datetime

schedule: dict = reading_schedule(IS_GOOGLE)  # Получение данных


def check_if_user_exists(telegram_id: int) -> bool:
	try:
		Database().session.query(User).where(User.telegram_id == telegram_id).one()
		return True
	except NoResultFound:
		return False


def add_new_user(telegram_id: int, telegram_name: str, role: RoleType, user_class: str) -> NoReturn:
	session = Database().session
	session.add(User(telegram_id=telegram_id, telegram_name=telegram_name, role=role, user_class=user_class))
	session.commit()


def get_user_by_id(telegram_id: int) -> User:
	return Database().session.query(User).where(User.telegram_id == telegram_id).one()


def add_extra_lesson(telegram_id: int, extra_lessons: str) -> str:
	texts = extra_lessons.split("\n")
	list_extra_lesson = []
	text_complete = "Расписание успешно добавлено!"

	count: int = 0

	for i, text in enumerate(texts):
		if text.count("=") == 2:
			split_text = text.split("=")
			start_time, end_time = split_text[2].split("-")

			list_extra_lesson.append([split_text[0], split_text[1], datetime.strptime(start_time, "%H:%M").time(),
									  datetime.strptime(end_time, "%H:%M").time()])
			count += 1
		else:
			text_complete = "Была добавлена только часть расписания, поскольку вы допустили ошибки в формате сообщения!"
	if 0 < count < len(texts):
		text_complete = "Была добавлена только часть расписания, поскольку вы допустили ошибки в формате сообщения!"
	elif count == 0:
		text_complete = "Вы допустили ошибки в формате сообщения! Расписание не было добавлено."

	user_id = get_user_by_id(telegram_id).id
	session = Database().session

	session.query(ExtraLesson).where(ExtraLesson.user_id == user_id).delete()

	list_extra_lesson_object: List[ExtraLesson] = [
		ExtraLesson(user_id=user_id, title=title, day=DaysOfWeek.week_day(day), time_start=start_time,
					time_end=end_time)
		for day, title, start_time, end_time in list_extra_lesson
	]
	session.add_all(list_extra_lesson_object)

	session.commit()
	return text_complete


def get_class(telegram_id: int) -> str:
	return Database().session.execute(select(User.user_class).where(User.telegram_id == telegram_id)).fetchone()[0]


def get_extra_lessons(telegram_id: int) -> List[List[str]]:
	user_id = Database().session.execute(select(User.id).where(User.telegram_id == telegram_id)).fetchone()[0]
	return Database().session.execute(
		select(ExtraLesson.day, ExtraLesson.title, ExtraLesson.time_start, ExtraLesson.time_end)
		.where(ExtraLesson.user_id == user_id)
	).fetchall()


def get_info_user(telegram_id: int) -> Tuple[str, RoleType, str, datetime]:
	return Database().session.execute(select(User.id, User.role, User.user_class, User.create_at)
									  .where(User.telegram_id == telegram_id)).fetchone()


def get_schedule_day(telegram_id: int, day_weekday: str) -> List[str]:
	return schedule[get_class(telegram_id)][day_weekday]


def delete_extra_lessons(telegram_id: int) -> NoReturn:
	session = Database().session
	user_id = get_user_by_id(telegram_id).id
	session.query(ExtraLesson).where(ExtraLesson.user_id == user_id).delete()
	session.commit()


def set_class(telegram_id: int, user_class: str) -> NoReturn:
	session = Database().session
	user = session.query(User).where(User.telegram_id == telegram_id).one()
	user.user_class = user_class
	session.commit()
