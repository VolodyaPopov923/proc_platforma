from aiogram import Router, types
from filters.is_admin import isAdmin
from filters.is_add_operator import isAddOperator
from database.db import add_operator
router = Router()


@router.message(isAdmin(), isAddOperator())
async def set_operator(message: types.Message):
    chat_id = message.chat.id
    username = message.text.split(" ")[1][1:]
    await add_operator(chat_id, username)
    await message.answer(f"Оператор @{username} добавлен")


@router.message(isAddOperator())
async def send_is_not_admin(message: types.Message):
    await message.answer("Вы не админ")
