import json
from os import getcwd, path

working_directory = getcwd()


def reading_schedule() -> {str: {str: []}}:
	with open(path.join(working_directory, "bot/database/schedules.json"), encoding="utf-8") as file:
		return json.load(file)


def reading_user_data() -> {str: {}}:
	with open(path.join(working_directory, "bot/database/user_data.json"), encoding="utf-8") as file:
		return json.load(file)


def write_file_user_data(data: {}):
	with open(path.join(working_directory, "bot/database/user_data.json"), "w", encoding="utf-8") as file:
		json.dump(data, file, ensure_ascii=False)
