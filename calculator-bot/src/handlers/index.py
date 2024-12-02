from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from handlers import balance
from handlers import calculator
from handlers.admin import index as admin
from handlers.operator import index as operator
from utils.send_info import send_info
from utils.send_help import send_help
from middleware.is_chat_on import isChatOnMiddleware
from database.db import (
    get_chat,
    add_chat,
    update_chat,
    set_balance,
    update_balance,
    set_payment,
    update_payment,
    set_rate,
    update_rate,
    set_course,
    update_course,
    set_deposit,
    update_deposit,
    clear_history,
)

router = Router()
router.include_router(admin.router)
router.include_router(operator.router)
router.include_router(balance.router)
router.include_router(calculator.router)

router.message.middleware(isChatOnMiddleware())

# Создание минибара
def create_reply_minibar():
    return ReplyKeyboardMarkup(
        keyboard=[
            # [KeyboardButton(text="🟢 Start")],
            [KeyboardButton(text="ℹ️ Info"), KeyboardButton(text="❓ Help")],
            [KeyboardButton(text="🔄 Restart"), KeyboardButton(text="⛔ Stop")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите команду из минибара",
    )

# Команда для вызова минибара
@router.message(Command(commands="minibar"))
async def cmd_minibar(message: types.Message):
    """
    Отображает минибар в строке ввода.
    """
    await message.answer(
        "Выберите команду из меню ниже 👇",
        reply_markup=create_reply_minibar(),
    )

# Общая функция для инициализации чата
async def initialize_chat(chat_id: int):
    await add_chat(chat_id)
    await set_balance(chat_id)
    await set_payment(chat_id)
    await set_rate(chat_id)
    await set_course(chat_id)
    await set_deposit(chat_id)

# Основные команды
@router.message(Command(commands="start"))
async def cmd_start(message: types.Message):
    chat_id = message.chat.id
    chat = await get_chat(chat_id)

    if not chat:
        await initialize_chat(chat_id)
        await message.answer(
            "База данных инициализирована.",
            reply_markup=create_reply_minibar(),
        )
        await send_help(message)
        return

    await update_chat(chat_id, True)
    await message.answer(
        "Бот запущен. Не забудьте изменить <b>депозит, курс и ставку</b>.",
        parse_mode="HTML",
        reply_markup=create_reply_minibar(),
    )

@router.message(Command(commands="info"))
async def cmd_info(message: types.Message):
    await send_info(message)

@router.message(Command(commands="help"))
async def cmd_help(message: types.Message):
    await send_help(message)

@router.message(Command(commands="restart"))
async def cmd_restart(message: types.Message):
    chat_id = message.chat.id
    chat = await get_chat(chat_id)

    if not chat:
        await initialize_chat(chat_id)
        await message.answer(
            "База данных инициализирована.",
            reply_markup=create_reply_minibar(),
        )
    else:
        await clear_history(chat_id)
        await update_balance(chat_id, 0, 0)
        await update_payment(chat_id, 0, 0)
        await update_rate(chat_id, 0)
        await update_course(chat_id, 90)
        await update_deposit(chat_id, 0)
        await update_chat(chat_id, True)
        await message.answer(
            "Бот перезапущен. Все параметры сброшены.",
            reply_markup=create_reply_minibar(),
        )
    await send_help(message)

@router.message(Command(commands="stop"))
async def cmd_stop(message: types.Message):
    chat_id = message.chat.id
    chat = await get_chat(chat_id)

    if chat:
        await clear_history(chat_id)
        await update_balance(chat_id, 0, 0)
        await update_payment(chat_id, 0, 0)
        await update_rate(chat_id, 0)
        await update_course(chat_id, 90)
        await update_deposit(chat_id, 0)
        await update_chat(chat_id, False)
        await message.answer(
            "Бот остановлен.",
            reply_markup=create_reply_minibar(),
        )
#
# @router.message(F.text == "🟢 Start")
# async def handle_start_button(message: types.Message):
#     await cmd_start(message)

@router.message(F.text == "ℹ️ Info")
async def handle_info_button(message: types.Message):
    await cmd_info(message)

@router.message(F.text == "❓ Help")
async def handle_help_button(message: types.Message):
    await cmd_help(message)

@router.message(F.text == "🔄 Restart")
async def handle_restart_button(message: types.Message):
    await cmd_restart(message)

@router.message(F.text == "⛔ Stop")
async def handle_stop_button(message: types.Message):
    await cmd_stop(message)
