from aiogram.types import Message
from typing import List, Dict
from database.db import get_chat


def get_history_text(history: List[Dict]):
    text = ""
    for i in range(len(history)):
        text += f"{history[i].date} <b>{history[i].num}</b>\n"
    return text


async def send_info(message: Message):
    chat_id = message.chat.id
    chat = await get_chat(chat_id)

    text = None

    if chat.history:
        text = get_history_text(chat.history)

    rub_bal_min_rate = chat.balance.rub - chat.balance.rub * chat.rate.rate * 0.01
    usdt_bal_min_rate = chat.balance.usdt - chat.balance.usdt * chat.rate.rate * 0.01

    await message.answer(
        (
            "Чеки:\n"
            f'{text if text else ""}\n'
            f"Депозит: <b>{chat.deposit.deposit}$</b>\n"
            f"Ставка трейдера: <b>{chat.rate.rate}%</b>\n"
            f"Курс: <b>{chat.course.course}$/₽</b>\n"
            f"Оборот: <b>{round(chat.balance.rub, 2)} | {round(chat.balance.usdt, 2)}$</b>\n"
            f"Оборот(-%): <b>{round(rub_bal_min_rate, 2)} | {round(usdt_bal_min_rate, 2)}$</b>\n"
            f"Выплаты: <b>{chat.payment.rub} | {chat.payment.usdt}$</b>\n"
            f"Осталось к выплате: <b>{round(rub_bal_min_rate - chat.payment.rub, 2)} | {round(usdt_bal_min_rate - chat.payment.usdt, 2)}$</b>"
        ),
        parse_mode="HTML",
    )
