import json
import os
from os import path
from typing import Final

from from_root import from_root

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_PATH = f"sqlite:///{from_root()}/src/resources/database.db"
SCHEDULES_PATH = path.join(from_root(), "src\\resources\\schedules.json")
PROFILE_PHOTOS_PATH = path.join(from_root(), "src\\resources\\profile_photos")
IS_GOOGLE = False

EFFECT_IDS: Final[dict[str: str]] = {
    "fire": "5104841245755180586",  # 🔥
    "like": "5107584321108051014",  # 👍
    "petard": "5046509860389126442",  # 🎉
    "heart": "5159385139981059251",  # ❤️
    "dislike": "5104858069142078462",  # 👎
    "poo": "5046589136895476101",  # 💩
}

with open(path.join(from_root(), "src\\resources\\users_role.json")) as file:
    data = json.load(file)

    ADMINS_ID: list[int] = data["admins"]
    BETA_TESTERS_ID: list[int] = data["beta_testers"]
    TEACHERS: dict[str: list[int]] = data["teachers"]
