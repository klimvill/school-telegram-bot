import json
from os import path
from typing import Final, Dict, List

from from_root import from_root
from gspread import authorize
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.resources.application import DATABASE_PATH
from src.resources.application import SCHEDULES_PATH


class Database:
	"""Класс, управляющий подключениями к бд."""
	BASE: Final = declarative_base()

	def __init__(self):
		self.__engine = create_engine(DATABASE_PATH)
		session = sessionmaker(bind=self.__engine)
		self.__session = session()

	@property
	def session(self):
		return self.__session

	@property
	def engine(self):
		return self.__engine


def reading_schedule(is_google: bool) -> Dict[str, Dict[str, List[str]]]:
	if is_google:
		scopes = [
			"https://www.googleapis.com/auth/spreadsheets",
			"https://www.googleapis.com/auth/drive"
		]

		credentials = ServiceAccountCredentials.from_json_keyfile_name(path.join(from_root(), "src\\resources\\private_key_google.json"), scopes)
		file = authorize(credentials)
		sheet = file.open("school telegram bot")

		table_columns = 39
		dict_schedule = {}

		all_class_schedule = sheet.sheet1.get_values(f"B1:AN77")

		for i in range(table_columns):
			processed_class_schedule = {}

			raw_class_schedule = [all_class_schedule[i_][i] for i_ in range(77)]

			processed_class_schedule["0"] = list(filter(lambda x: x != "-", raw_class_schedule[1:11]))
			processed_class_schedule["1"] = list(filter(lambda x: x != "-", raw_class_schedule[12:22]))
			processed_class_schedule["2"] = list(filter(lambda x: x != "-", raw_class_schedule[23:33]))
			processed_class_schedule["3"] = list(filter(lambda x: x != "-", raw_class_schedule[34:44]))
			processed_class_schedule["4"] = list(filter(lambda x: x != "-", raw_class_schedule[45:55]))
			processed_class_schedule["5"] = list(filter(lambda x: x != "-", raw_class_schedule[56:66]))
			processed_class_schedule["6"] = list(filter(lambda x: x != "-", raw_class_schedule[67:77]))
			dict_schedule[raw_class_schedule[0]] = processed_class_schedule

		print("Расписание получено…")
		return dict_schedule
	else:
		with open(SCHEDULES_PATH, encoding="utf-8") as file:
			return json.load(file)
