from aiogram import Router, types
from filters.is_calc_operation import isCalcOperation
from database.db import get_course

router = Router()


@router.message(isCalcOperation())
async def calculate(message: types.Message):
    text = message.text
    chat_id = message.chat.id

    course_data = await get_course(chat_id)
    course = course_data.course if course_data else 1
    tokens = text.split()
    processed_tokens = []
    for token in tokens:
        if token.lower() == 'курс':
            processed_tokens.append(str(course))
        else:
            processed_tokens.append(token)

    expression = ' '.join(processed_tokens)

    try:
        allowed_names = {
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
        }
        result = eval(expression, {"__builtins__": None}, allowed_names)
    except ZeroDivisionError:
        result = 'Математику учил?'
    except Exception:
        result = 'Вы где-то накосячили'

    await message.answer(f'{result}')
