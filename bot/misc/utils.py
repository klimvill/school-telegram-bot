from datetime import datetime, time


def get_lesson_number(number_lessons: int):
	"""Получение номера текущего урока"""
	current_time = datetime.now().time()

	if time(0, 0) <= current_time <= time(8, 0): lesson = 'Уроки не начались'
	elif time(8, 0) <= current_time <= time(8, 40): lesson = 0
	elif time(8, 40) <= current_time <= time(9, 35) and number_lessons >= 2: lesson = 1
	elif time(9, 35) <= current_time <= time(10, 30) and number_lessons >= 3: lesson = 2
	elif time(10, 30) <= current_time <= time(11, 25) and number_lessons >= 4: lesson = 3
	elif time(11, 25) <= current_time <= time(12, 20) and number_lessons >= 5: lesson = 4
	elif time(12, 20) <= current_time <= time(13, 10) and number_lessons >= 6: lesson = 5
	elif time(13, 10) <= current_time <= time(13, 55) and number_lessons >= 7: lesson = 6
	elif time(13, 55) <= current_time <= time(15, 00) and number_lessons >= 8: lesson = 7
	elif time(15, 00) <= current_time <= time(15, 45) and number_lessons >= 9: lesson = 8
	else: lesson = 'Уроки кончились'

	return lesson


def create_schedule(date: str, schedule_day: list[str]):
	"""Создание текста расписания"""
	count: int = 1

	text_message = f'📆 *Расписание уроков на {date}*\n'
	number_current_lesson = get_lesson_number(len(schedule_day))

	if schedule_day != 'Выходной':  # len(schedule_day) != 0
		if number_current_lesson in ('Уроки не начались', 'Уроки кончились'): ...
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
	else: text_message += "\nВыходной"

	return text_message


def create_short_schedule(day_week: str, schedule_day: list[str]):
	"""Создание сокращённого текста расписания"""
	count: int = 1
	text_message = f'📆 *Расписание уроков на {day_week}*\n'

	if schedule_day != 'Выходной':  # len(schedule_day) != 0
		for value in schedule_day:
			if value == '':
				text_message += '\n\n*Внеурочки*'
			else:
				text_message += f'\n{count}. {value}'
				count += 1  # Через enumerate сделать не получится, потому что нужен пропуск (см. выше)
	else: text_message += '\nВыходной'

	return text_message
