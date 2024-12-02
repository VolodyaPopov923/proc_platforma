from aiogram.types import Message
from aiogram.filters import BaseFilter
from utils.is_float import is_float


class isSetPayment(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            text = message.text.split(" ")
            if (
                len(text) == 2
                and text[0].lower() in ["выплаты", "выплата"]
                and is_float(text[1])
            ):
                return True
            else:
                return False
        except:
            return False
