from aiogram.types import Message
from aiogram.filters import BaseFilter
from utils.is_float import is_float


class isCalcOperation(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            text = message.text.split(' ')
            num_1 = text[0]
            sign = text[1]
            num_2 = text[2]

            if (
                len(text) >= 3
                and (sign in ['+', '-', '/', '*'])
                and is_float(num_1)
                and (is_float(num_2) or num_2.lower() == 'курс')
            ):
                return True
            else:
                return False
        except:
            return False