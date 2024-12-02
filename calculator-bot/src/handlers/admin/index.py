from aiogram import Router

from handlers.admin import add_operator
from handlers.admin import delete_operator

router = Router()

router.include_router(add_operator.router)
router.include_router(delete_operator.router)
