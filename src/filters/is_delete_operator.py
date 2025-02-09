from aiogram.types import Message
from aiogram.filters import BaseFilter


class isDeleteOperator(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        text = message.text.split(" ")
        if len(text) == 2 and text[0].lower() == "удалить" and text[1][0] == "@":
            return True
        else:
            return False
