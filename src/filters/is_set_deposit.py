from aiogram.types import Message
from aiogram.filters import BaseFilter
from utils.is_float import is_float


class isSetDeposit(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            text = message.text.split(" ")
            sign = text[1][0]
            num = text[1][1:]
            if (
                len(text) == 2
                and (text[0].lower() == "депозит")
                and (sign == "+" or sign == "-")
                and is_float(num)
            ):
                return True
            else:
                return False
        except:
            return False
