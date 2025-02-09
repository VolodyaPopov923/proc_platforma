from aiogram import Router, types
from filters.is_set_payment import isSetPayment
from filters.is_operator import isOperator
from utils.to_float import to_float
from utils.send_info import send_info
from database.db import get_course, get_payment, update_payment
from utils.send_forbidden import send_forbidden

router = Router()


@router.message(isOperator(), isSetPayment())
async def change_balance(message: types.Message):
    chat_id = message.chat.id
    num = to_float(message.text.split(" ")[1])
    course = (await get_course(chat_id)).course
    payment = await get_payment(chat_id)

    rub_payment = payment.rub + num * course
    usdt_payment = payment.usdt + num

    await update_payment(chat_id, rub_payment, usdt_payment)

    await send_info(message)


@router.message(isSetPayment())
async def send_is_not_operator(message: types.Message):
    await send_forbidden(message)
