from aiogram.types import Message
from aiogram.filters import BaseFilter


class isAddOperator(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        text = message.text.split(" ")
        if len(text) == 2 and text[0].lower() == "оператор" and text[1][0] == "@":
            return True
        else:
            return False