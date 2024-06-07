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


def get_class(user_id: int):
	return reading_user_data()[str(user_id)]['class']


def get_schedule_day(user_id: int, day_weekday: str):
	return reading_schedule()[get_class(user_id)][day_weekday]
