import os
from os import path, getcwd

from from_root import from_root

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_PATH = f"sqlite:///{from_root()}/src/resources/database.db"
SCHEDULES_PATH = path.join(from_root(), "src\\resources\\schedules.json")
