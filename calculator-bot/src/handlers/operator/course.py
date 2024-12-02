from aiogram import Router, types
from filters.is_set_course import isSetCourse
from filters.is_operator import isOperator
from database.db import update_course
from utils.to_float import to_float
from utils.send_info import send_info
from utils.send_forbidden import send_forbidden

router = Router()


@router.message(isOperator(), isSetCourse())
async def set_course(message: types.Message):
    chat_id = message.chat.id
    course = to_float(message.text.split(" ")[1])
    print(message.from_user.id)
    await update_course(chat_id, course)
    await send_info(message)


@router.message(isSetCourse())
async def send_is_not_operator(message: types.Message):
    await send_forbidden(message)
