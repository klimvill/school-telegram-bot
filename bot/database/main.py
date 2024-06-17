import json
from os import getcwd, path

from gspread import authorize
from oauth2client.service_account import ServiceAccountCredentials

working_directory = getcwd()

scopes = [
	"https://www.googleapis.com/auth/spreadsheets",
	"https://www.googleapis.com/auth/drive"
]

credentials = ServiceAccountCredentials.from_json_keyfile_name("bot/misc/private_key_google.json", scopes)
file = authorize(credentials)
sheet = file.open("Python_MUO_Google_Sheet")


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


def reading_user_data() -> dict[str: dict]:
	with open(path.join(working_directory, "bot/database/user_data.json"), encoding="utf-8") as file:
		return json.load(file)


def write_file_user_data(data: dict):
	with open(path.join(working_directory, "bot/database/user_data.json"), "w", encoding="utf-8") as file:
		json.dump(data, file, ensure_ascii=False)
