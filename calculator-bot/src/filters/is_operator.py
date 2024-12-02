from aiogram.types import Message
from aiogram.filters import BaseFilter
from database.db import get_operator_by_chat_id


class isOperator(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        operator = await get_operator_by_chat_id(
            message.chat.id, message.from_user.username
        )
        if operator:
            return True
        else:
            return False
