from aiogram import Router
from .admin import router as admin_router
from .start import router as start_router
from .info import router as info_router
from .anketa import router as anketa_router

main_router = Router(name="main_router")

# Routerlarni ro'yxatga olish
main_router.include_router(admin_router)
main_router.include_router(start_router)
main_router.include_router(info_router)
main_router.include_router(anketa_router)

__all__ = ["main_router"]
