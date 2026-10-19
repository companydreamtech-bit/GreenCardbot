import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config import config
from database import db
from handlers import main_router
from utils.scheduler import run_reminder_scheduler

# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("GreenCardBot")

scheduler_task = None


async def set_bot_commands(bot: Bot):
    """Bot uchun rasmiy menyu buyruqlarini o'rnatish"""
    commands = [
        BotCommand(command="start", description="Botni qayta ishga tushirish / Перезапустить бот"),
        BotCommand(command="lang", description="Tilni o'zgartirish / Сменить язык"),
        BotCommand(command="stats", description="Admin: Statistika"),
        BotCommand(command="broadcast", description="Admin: Rassilka"),
    ]
    await bot.set_my_commands(commands)


async def on_startup(bot: Bot):
    """Bot ishga tushganda bajariladigan amallar"""
    global scheduler_task
    logger.info("Initializing database...")
    await db.init_db()

    await set_bot_commands(bot)

    # Avtomatik eslatmalar fon jarayonini ishga tushirish
    scheduler_task = asyncio.create_task(run_reminder_scheduler(bot))

    bot_info = await bot.get_me()
    logger.info(f"Bot @{bot_info.username} muvaffaqiyatli ishga tushdi!")

    # Admin guruhiga bildirishnoma
    try:
        if config.ADMIN_GROUP_ID:
            await bot.send_message(
                chat_id=config.ADMIN_GROUP_ID,
                text=f"🟢 <b>Green Card DV-2027 Boti ishga tushdi!</b>\n🤖 Bot: @{bot_info.username}",
                parse_mode=ParseMode.HTML,
            )
    except Exception as e:
        logger.warning(f"Admin guruhiga xabar jo'natilmadi: {e}")


async def on_shutdown(bot: Bot):
    """Bot to'xtatilganda bajariladigan amallar"""
    global scheduler_task
    logger.info("Bot to'xtatilmoqda...")
    if scheduler_task and not scheduler_task.done():
        scheduler_task.cancel()

    try:
        if config.ADMIN_GROUP_ID:
            await bot.send_message(
                chat_id=config.ADMIN_GROUP_ID,
                text="🔴 <b>Green Card DV-2027 Boti to'xtatildi.</b>",
                parse_mode=ParseMode.HTML,
            )
    except Exception:
        pass


async def main():
    if not config.BOT_TOKEN or config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error(
            "XATOLIK: .env faylida BOT_TOKEN ko'rsatilmagan! Iltimos, .env faylini to'ldiring."
        )
        sys.exit(1)

    # Bot va Dispatcher yaratish
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Handlers routerini ulash
    dp.include_router(main_router)

    # Startup va Shutdown hodisalari
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Eskirgan yangilanishlarni (updates) tozalab, pollingni boshlash
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi.")
