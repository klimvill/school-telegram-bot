import sqlite3

from gspread import authorize
from oauth2client.service_account import ServiceAccountCredentials

scopes = [
	"https://www.googleapis.com/auth/spreadsheets",
	"https://www.googleapis.com/auth/drive"
]

credentials = ServiceAccountCredentials.from_json_keyfile_name("bot/config/private_key_google.json", scopes)
file = authorize(credentials)
sheet = file.open("school telegram bot")


def reading_schedule() -> dict[str: dict[str: list[str]]]:
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

	print("Расписание получено...")
	return dict_schedule


user_db = sqlite3.connect('bot/database/users_data.db')
cursor = user_db.cursor()


def register_db():
	cursor.execute('''CREATE TABLE IF NOT EXISTS users (
		"telegram_id" INTEGER NOT NULL UNIQUE,
		"role" TEXT NOT NULL,
		"class" TEXT NOT NULL,
		"date_registration"	TEXT NOT NULL,
		"extra_lessons" TEXT NOT NULL,
		"progress" TEXT NOT NULL
	)''')
	user_db.commit()
