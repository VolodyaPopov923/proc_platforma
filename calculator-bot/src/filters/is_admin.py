from aiogram.types import Message
from aiogram.filters import BaseFilter
from config import ADMINS


class isAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id in ADMINS:
            return True
        else:
            return False
