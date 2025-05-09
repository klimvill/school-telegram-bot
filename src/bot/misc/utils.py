from datetime import datetime, time
from typing import Union, List

from src.bot.db.enums import DaysOfWeek
from src.bot.db.methods import get_extra_lessons


def get_lesson_number(number_lessons: int) -> Union[int, str]:
	"""Получение номера текущего урока"""
	current_time = datetime.now().time()

	if time(0, 0) <= current_time <= time(8, 0):
		lesson = 'Уроки не начались'
	elif time(8, 0) <= current_time <= time(8, 40):
		lesson = 0
	elif time(8, 40) <= current_time <= time(9, 35) and number_lessons >= 2:
		lesson = 1
	elif time(9, 35) <= current_time <= time(10, 30) and number_lessons >= 3:
		lesson = 2
	elif time(10, 30) <= current_time <= time(11, 25) and number_lessons >= 4:
		lesson = 3
	elif time(11, 25) <= current_time <= time(12, 20) and number_lessons >= 5:
		lesson = 4
	elif time(12, 20) <= current_time <= time(13, 10) and number_lessons >= 6:
		lesson = 5
	elif time(13, 10) <= current_time <= time(13, 55) and number_lessons >= 7:
		lesson = 6
	elif time(13, 55) <= current_time <= time(15, 00) and number_lessons >= 8:
		lesson = 7
	elif time(15, 00) <= current_time <= time(15, 45) and number_lessons >= 9:
		lesson = 8
	else:
		lesson = 'Уроки кончились'

	return lesson


def create_schedule(date: str, schedule_day: List[str]) -> str:
	"""Создание текста расписания"""
	count: int = 1

	text_message = f'📆 *Расписание уроков на {date}*\n'
	number_current_lesson = get_lesson_number(len(schedule_day))

	if len(schedule_day) != 0:
		if number_current_lesson in ('Уроки не начались', 'Уроки кончились'):
			...
		elif schedule_day[number_current_lesson] == "":  # Внеурочки от уроков отделяются пустой строчкой в списке
			number_current_lesson += 1

		if number_current_lesson == 'Уроки кончились':
			text_message += '\n*Уроки кончились*\n'
		elif number_current_lesson == 'Уроки не начались':
			text_message += f'\n*Будет - {schedule_day[0]}*\n'
		else:
			text_message += f'\n*Сейчас - {schedule_day[number_current_lesson]}*\n'

		for value in schedule_day:
			if value == '':
				text_message += '\n\n*Внеурочки*'
			else:
				text_message += f'\n{count}. {value}'
				count += 1  # Через enumerate сделать не получится, потому что нужен пропуск (см. выше)
	else:
		text_message += "\nВыходной"

	return text_message


def create_short_schedule(day_week: str, schedule_day: List[str]) -> str:
	"""Создание сокращённого текста расписания"""
	count: int = 1
	text_message = f'📆 *Расписание уроков на {day_week}*\n'

	if len(schedule_day) != 0:
		for value in schedule_day:
			if value == '' and text_message == f'📆 *Расписание уроков на {day_week}*\n':
				text_message += '\n*Внеурочки*'
			elif value == '':
				text_message += '\n\n*Внеурочки*'
			else:
				text_message += f'\n{count}. {value}'
				count += 1  # Через enumerate сделать не получится, потому что нужен пропуск (см. выше)
	else:
		text_message += '\nВыходной'

	return text_message


def create_extra_lesson(user_id: int) -> str:
	saved_day_week = None
	text_message = '📆 *Расписание дополнительных занятий*\n'
	extra_lessons = get_extra_lessons(user_id)

	if not extra_lessons:
		text_message += '\nРасписание не добавлено\n'
	else:
		extra_lessons = (
			list((DaysOfWeek.to_string(day), title, start_time, end_time))
			for day, title, start_time, end_time in extra_lessons
		)

		try:
			day_order = ('понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье')
			extra_lessons = sorted(extra_lessons, key=lambda d: day_order.index(d[0].lower()))
			sorted_extra_lessons = {
				day: [extra_lesson for extra_lesson in extra_lessons if extra_lesson[0].lower() == day]
				for day in day_order
			}

			for day_week, extra_lessons in sorted_extra_lessons.items():
				if extra_lessons:
					text_message += f"\n*{extra_lessons[0][0]}*\n"

				for extra_lesson in sorted(extra_lessons, key=lambda e: e[2]):
					text_message += f"{extra_lesson[1]} ({extra_lesson[2].strftime('%H:%M')}-{extra_lesson[3].strftime('%H:%M')})\n"

		except ValueError:  # если ключ не найден не сортируем
			for these_classes in extra_lessons:
				day_week = these_classes[0]

				if saved_day_week != day_week:
					text_message += f"\n*{day_week}*\n"
					saved_day_week = day_week
				text_message += f"{these_classes[1]} ({these_classes[2].strftime('%H:%M')}-{these_classes[3].strftime('%H:%M')})\n"

	text_message += "\n👇 Вы также можете посмотреть расписание на сегодня"
	return text_message
