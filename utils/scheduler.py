import asyncio
import logging
from aiogram import Bot
from database import db
from locales.texts import get_text
from config import config

logger = logging.getLogger(__name__)


async def run_reminder_scheduler(bot: Bot):
    """To'lov qilinmagan arizalar uchun avtomatik fon eslatuvchisi (har 30 daqiqada tekshiradi)"""
    logger.info("Reminder scheduler started.")
    while True:
        try:
            # 30 daqiqa kutish
            await asyncio.sleep(1800)

            unpaid_apps = await db.get_unpaid_applications_for_reminder()
            for app in unpaid_apps:
                user_id = app["user_id"]
                lang = app.get("language", "uz")
                app_code = app["application_code"]
                user_name = app.get("user_name", "Foydalanuvchi")

                text = get_text(
                    lang,
                    "reminder_unpaid",
                    name=user_name,
                    app_code=app_code,
                    card_number=config.PAYMENT_CARD_NUMBER,
                    card_holder=config.PAYMENT_CARD_HOLDER,
                )

                try:
                    await bot.send_message(chat_id=user_id, text=text, parse_mode="HTML")
                    await db.mark_reminder_sent(app_code)
                    logger.info(f"Sent payment reminder for app {app_code} to user {user_id}")
                except Exception as e:
                    logger.warning(f"Could not send reminder to {user_id}: {e}")

        except asyncio.CancelledError:
            logger.info("Reminder scheduler stopped.")
            break
        except Exception as e:
            logger.error(f"Error in reminder scheduler: {e}", exc_info=True)
            await asyncio.sleep(60)
