from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.resources.application import ADMINS_ID, BETA_TESTERS_ID, TEACHERS


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMINS_ID


class IsBetaTester(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in BETA_TESTERS_ID


class IsTeacher(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return str(message.from_user.id) in TEACHERS
