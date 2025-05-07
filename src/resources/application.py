import json
import os
from os import path

from from_root import from_root

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_PATH = f"sqlite:///{from_root()}/src/resources/database.db"
SCHEDULES_PATH = path.join(from_root(), "src\\resources\\schedules.json")
IS_GOOGLE = False

with open(path.join(from_root(), "src\\resources\\users_role.json")) as file:
    data = json.load(file)

    ADMINS_ID: list[int] = data["admins"]
    BETA_TESTERS_ID: list[int] = data["beta_testers"]
    TEACHERS: dict[str: list[int]] = data["teachers"]
