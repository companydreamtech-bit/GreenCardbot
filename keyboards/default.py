from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from locales.texts import get_text
from config import config


def get_main_menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """Asosiy menyu klaviaturasi (Status, Referal va Web App bilan)"""
    kb = [
        [
            KeyboardButton(text=get_text(lang, "btn_anketa")),
            KeyboardButton(
                text=get_text(lang, "btn_website"),
                web_app=WebAppInfo(url=config.WEB_APP_URL),
            ),
        ],
        [
            KeyboardButton(text=get_text(lang, "btn_my_status")),
            KeyboardButton(text=get_text(lang, "btn_referral")),
        ],
        [
            KeyboardButton(text=get_text(lang, "btn_photo_rules")),
            KeyboardButton(text=get_text(lang, "btn_pricing")),
        ],
        [
            KeyboardButton(text=get_text(lang, "btn_faq")),
            KeyboardButton(text=get_text(lang, "btn_change_lang")),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Bo'limlardan birini tanlang..." if lang == "uz" else "Выберите раздел...",
    )


def get_phone_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """Telefon raqam yuborish va bekor qilish klaviaturasi"""
    kb = [
        [
            KeyboardButton(
                text=get_text(lang, "btn_send_contact"),
                request_contact=True,
            )
        ],
        [
            KeyboardButton(text=get_text(lang, "btn_cancel")),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)


def get_skip_patronymic_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """Otasi ismini o'tkazib yuborish yoki bekor qilish klaviaturasi"""
    kb = [
        [
            KeyboardButton(text=get_text(lang, "btn_skip_patronymic")),
        ],
        [
            KeyboardButton(text=get_text(lang, "btn_cancel")),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)


def get_cancel_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """Faqat bekor qilish tugmasi"""
    kb = [
        [
            KeyboardButton(text=get_text(lang, "btn_cancel")),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
