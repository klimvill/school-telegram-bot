import json
from datetime import date
from locale import setlocale, LC_ALL
from typing import Any, NoReturn

from .main import user_db, cursor, reading_schedule

setlocale(category=LC_ALL, locale="Russian")  # Настройка локализации для правильной работы datetime

# Получение данных
schedule: dict = reading_schedule()


def check_if_user_exists(user_id: int) -> bool:
	if cursor.execute(f'SELECT * FROM users WHERE telegram_id="{user_id}"').fetchone() is None:
		return False
	return True


def add_new_user(user_id: int, data: dict[str, Any]) -> NoReturn:
	cursor.execute(f'''INSERT INTO users VALUES (
		'{user_id}', 
		'Ученик', 
		'{data['class_number']}', 
		'{date.today().strftime('%d %b. %Y')}',
		'[]',
		'[]'
	)''')
	user_db.commit()


def add_extra_lesson(user_id: int, data: dict[str, Any]) -> str:
	text = data['extra_lesson'].split("\n")
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

	extra_lesson_text = json.dumps(list_extra_lesson, ensure_ascii=False)  # Превращаем список в строку
	cursor.execute(f'''UPDATE users SET extra_lessons = '{extra_lesson_text}' WHERE telegram_id = {user_id}''')
	user_db.commit()

	return text_complete


def get_class(user_id: int) -> str:
	return cursor.execute(f'SELECT class FROM users WHERE telegram_id = {user_id}').fetchone()[0]


def get_extra_lesson(user_id: int) -> list[list[str]]:
	return json.loads(cursor.execute(f'SELECT extra_lessons FROM users WHERE telegram_id = {user_id}').fetchone()[0])


def get_info_student(user_id: int) -> tuple[str, str, str, str]:
	return cursor.execute(f'SELECT rowid, role, class, date_registration FROM users WHERE telegram_id = "{user_id}"').fetchone()


def get_schedule_day(user_id: int, day_weekday: str) -> list[str]:
	return schedule[get_class(user_id)][day_weekday]


def delete_extra_lesson(user_id: int) -> NoReturn:
	cursor.execute(f'UPDATE users SET extra_lessons = "[]" WHERE telegram_id = "{user_id}"')
	user_db.commit()


def set_class(user_id: int, class_: str) -> NoReturn:
	cursor.execute(f'UPDATE users SET class = "{class_}" WHERE telegram_id = "{user_id}"')
	user_db.commit()
