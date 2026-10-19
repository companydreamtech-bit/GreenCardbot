import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    ADMIN_GROUP_ID: int = int(os.getenv("ADMIN_GROUP_ID", "-1004332225482"))
    ADMIN_IDS: list[int] = None
    WEB_APP_URL: str = os.getenv("WEB_APP_URL", "https://greencard-dv2027.vercel.app")
    CHANNEL_USERNAME: str = os.getenv("CHANNEL_USERNAME", "@greencarddv_2027")
    
    PAYMENT_CARD_NUMBER: str = os.getenv("PAYMENT_CARD_NUMBER", "8600 0000 0000 0000")
    PAYMENT_CARD_HOLDER: str = os.getenv("PAYMENT_CARD_HOLDER", "GREEN CARD ADMIN")
    PAYMENT_PHONE: str = os.getenv("PAYMENT_PHONE", "+998901234567")
    
    DB_PATH: str = os.getenv("DB_PATH", "greencard.db")

    def __post_init__(self):
        admin_ids_str = os.getenv("ADMIN_IDS", "")
        self.ADMIN_IDS = [
            int(item.strip()) for item in admin_ids_str.split(",") if item.strip().isdigit()
        ]


config = Settings()
