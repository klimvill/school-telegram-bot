from datetime import date
from locale import setlocale, LC_ALL
from typing import Any

from .main import *

setlocale(category=LC_ALL, locale="Russian")  # Настройка локализации для правильной работы datetime


def check_if_user_exists(user_id: int):
	if str(user_id) in reading_user_data():
		return True
	return False


def add_new_user(user_id: int, user_data: dict[str, Any]):
	data = reading_user_data()

	data[str(user_id)] = {
		"id": len(data) + 1,
		"role": "Ученик",
		"class": user_data['class_number'],
		"extra lessons": [],
		"date registration": f"{date.today().strftime('%d %b. %Y')}"
	}

	write_file_user_data(data)


def add_extra_lesson(user_id: int, user_data: dict[str, Any]) -> str:
	text = user_data['extra_lesson'].split("\n")
	data = reading_user_data()
	list_extra_lesson = []
	text_complete = "Расписание успешно добавлено!"

	count: int = 0

	for i in range(len(text)):
		if text[i].count("=") == 2:
			list_extra_lesson.append(text[i].split("="))
			count += 1
		else:
			text_complete = "Была добавлена только часть расписания, поскольку вы допустили ошибки в формате сообщения!"
	if 0 < count < len(text):
		text_complete = "Была добавлена только часть расписания, поскольку вы допустили ошибки в формате сообщения!"
	elif count == 0:
		text_complete = "Вы допустили ошибки в формате сообщения! Расписание не было добавлено."

	data[str(user_id)]['extra lessons'] = list_extra_lesson
	write_file_user_data(data)
	return text_complete


def delete_extra_lesson(user_id: int) -> None:
	data = reading_user_data()
	data[str(user_id)]['extra lessons'] = []
	write_file_user_data(data)


def get_class(user_id: int):
	return reading_user_data()[str(user_id)]['class']


def get_schedule_day(user_id: int, day_weekday: str):
	return reading_schedule()[get_class(user_id)][day_weekday]


def get_extra_lesson(user_id: int):
	return reading_user_data()[str(user_id)]['extra lessons']


def get_info_student(user_id: int):
	user_id = str(user_id)
	user_data = reading_user_data()

	return (user_data[user_id]['id'], user_data[user_id]['role'],
			user_data[user_id]['class'], user_data[user_id]['date registration'])


def set_class(user_id: int, class_: str):
	data = reading_user_data()
	data[str(user_id)]['class'] = class_
	write_file_user_data(data)
