from aiogram import Router, types
from filters.is_set_rate import isSetRate
from filters.is_operator import isOperator
from database.db import update_rate
from utils.to_float import to_float
from utils.send_info import send_info
from utils.send_forbidden import send_forbidden

router = Router()


@router.message(isOperator(), isSetRate())
async def set_course(message: types.Message):
    rate = to_float(message.text.split(" ")[1])
    await update_rate(message.chat.id, rate)
    await send_info(message)


@router.message(isSetRate())
async def send_is_not_operator(message: types.Message):
    await send_forbidden(message)
