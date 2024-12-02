from aiogram import Router, types
from filters.is_set_balance import isSetBalance
from utils.to_float import to_float
from utils.send_info import send_info
from database.db import get_course, get_balance, update_balance, update_history
import datetime

router = Router()


@router.message(isSetBalance())
async def change_balance(message: types.Message):
    chat_id = message.chat.id
    sign = message.text[0]
    num = to_float(message.text[1:])
    course = (await get_course(chat_id)).course
    balance = await get_balance(chat_id)

    if sign == "+":
        rub_balance = balance.rub + num
        usdt_balance = balance.usdt + num / course
    else:
        rub_balance = balance.rub - num
        usdt_balance = balance.usdt - num / course

    await update_balance(chat_id, rub_balance, usdt_balance)

    await update_history(
        chat_id, datetime.datetime.now().strftime("%H:%M:%S"), f"{sign}{num}"
    )

    await send_info(message)
