from aiogram.types import Message


async def send_forbidden(message: Message):
    await message.answer("Вы не оператор")