from aiogram import Router, types
from filters.is_admin import isAdmin
from filters.is_delete_operator import isDeleteOperator
from database.db import delete_operator
router = Router()


@router.message(isAdmin(), isDeleteOperator())
async def set_operator(message: types.Message):
    username = message.text.split(" ")[1][1:]
    await delete_operator(username)
    await message.answer(f"Оператор @{username} удален")


@router.message(isDeleteOperator())
async def send_is_not_admin(message: types.Message):
    await message.answer("Вы не админ")
