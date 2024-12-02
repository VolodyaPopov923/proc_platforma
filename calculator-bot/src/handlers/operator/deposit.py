from aiogram import Router, types
from filters.is_set_deposit import isSetDeposit
from filters.is_operator import isOperator
from utils.to_float import to_float
from database.db import get_deposit, update_deposit
from utils.send_info import send_info
from utils.send_forbidden import send_forbidden

router = Router()


@router.message(isOperator(), isSetDeposit())
async def change_deposit(message: types.Message):
    chat_id = message.chat.id
    text = message.text.split(" ")
    sign = text[1][0]
    print(to_float(text[1][1:]))
    num = to_float(text[1][1:])
    deposit = (await get_deposit(chat_id)).deposit

    if sign == "+":
        deposit = deposit + num
    else:
        deposit = deposit - num

    await update_deposit(chat_id, deposit)

    await send_info(message)


@router.message(isSetDeposit())
async def send_is_not_operator(message: types.Message):
    await send_forbidden(message)
