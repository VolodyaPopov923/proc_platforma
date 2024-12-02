from aiogram.types import Message
from aiogram.filters import BaseFilter
from utils.is_float import is_float


class isSetBalance(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            sign = message.text[0]
            num = message.text[1:]
            if (
                len(message.text.split(" ")) == 1
                and (sign == "-" or sign == "+")
                and is_float(num)
            ):
                return True
            else:
                return False
        except:
            return False
