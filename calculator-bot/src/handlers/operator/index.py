from aiogram import Router

from handlers.operator import deposit, payment, rate, course

router = Router()

router.include_router(deposit.router)
router.include_router(course.router)
router.include_router(rate.router)
router.include_router(payment.router)
