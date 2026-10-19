from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from locales.texts import get_text
import re


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Tilni tanlash uchun inline klaviatura"""
    buttons = [
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="set_lang:uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang:ru"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_gender_keyboard(lang: str, prefix: str = "main") -> InlineKeyboardMarkup:
    """Jinsni tanlash inline klaviaturasi"""
    buttons = [
        [
            InlineKeyboardButton(
                text=get_text(lang, "btn_male"), callback_data=f"{prefix}_gender:male"
            ),
            InlineKeyboardButton(
                text=get_text(lang, "btn_female"), callback_data=f"{prefix}_gender:female"
            ),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_education_keyboard(lang: str, prefix: str = "main") -> InlineKeyboardMarkup:
    """Ta'lim darajasini tanlash inline klaviaturasi"""
    buttons = [
        [
            InlineKeyboardButton(
                text=get_text(lang, "edu_primary"), callback_data=f"{prefix}_edu:primary"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text(lang, "edu_college"), callback_data=f"{prefix}_edu:college"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text(lang, "edu_bachelor"), callback_data=f"{prefix}_edu:bachelor"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text(lang, "edu_master"), callback_data=f"{prefix}_edu:master"
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_marital_status_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Oilaviy holatni tanlash inline klaviaturasi"""
    buttons = [
        [
            InlineKeyboardButton(
                text=get_text(lang, "status_single"), callback_data="marital:single"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text(lang, "status_married"), callback_data="marital:married"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text(lang, "status_divorced"), callback_data="marital:divorced"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text(lang, "status_widowed"), callback_data="marital:widowed"
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_children_count_keyboard() -> InlineKeyboardMarkup:
    """Bolalar sonini tanlash (0 dan 5 gacha) inline klaviaturasi"""
    buttons = [
        [
            InlineKeyboardButton(text="0", callback_data="children_count:0"),
            InlineKeyboardButton(text="1", callback_data="children_count:1"),
            InlineKeyboardButton(text="2", callback_data="children_count:2"),
        ],
        [
            InlineKeyboardButton(text="3", callback_data="children_count:3"),
            InlineKeyboardButton(text="4", callback_data="children_count:4"),
            InlineKeyboardButton(text="5", callback_data="children_count:5"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_review_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Anketa yakunida tasdiqlash yoki qayta to'ldirish klaviaturasi"""
    buttons = [
        [
            InlineKeyboardButton(
                text=get_text(lang, "btn_confirm"), callback_data="review:confirm"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text(lang, "btn_restart"), callback_data="review:restart"
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_admin_user_action_keyboard(
    app_code: str, user_id: int, username: str = None, phone: str = None
) -> InlineKeyboardMarkup:
    """Admin guruhidagi arizani 1 tugma bilan boshqarish tugmalari"""
    buttons = [
        # 1-qator: Admin harakatlari (1-Click Actions)
        [
            InlineKeyboardButton(
                text="💳 To'lovni tasdiqlash", callback_data=f"adm_pay:{app_code}:{user_id}"
            ),
            InlineKeyboardButton(
                text="📄 Confirmation kiritish", callback_data=f"adm_conf:{app_code}:{user_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="❌ Rad etish", callback_data=f"adm_rej:{app_code}:{user_id}"
            ),
        ],
    ]

    # 2-qator: Aloqa tugmalari
    comm_row = []
    if username:
        comm_row.append(
            InlineKeyboardButton(
                text=f"💬 @{username.replace('@', '')}",
                url=f"https://t.me/{username.replace('@', '')}",
            )
        )
    else:
        comm_row.append(
            InlineKeyboardButton(text="💬 Profil (ID)", url=f"tg://user?id={user_id}")
        )

    if phone:
        clean_num = re.sub(r"[^\d+]", "", phone)
        comm_row.append(
            InlineKeyboardButton(text=f"📞 Tel ({clean_num})", url=f"https://t.me/{clean_num}")
        )

    buttons.append(comm_row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_broadcast_lang_keyboard() -> InlineKeyboardMarkup:
    """Broadcast uchun auditoriya tanlash"""
    buttons = [
        [
            InlineKeyboardButton(text="🇺🇿 Faqat O'zbekcha", callback_data="bc_lang:uz"),
            InlineKeyboardButton(text="🇷🇺 Faqat Ruscha", callback_data="bc_lang:ru"),
        ],
        [
            InlineKeyboardButton(text="🌐 Barchaga yuborish", callback_data="bc_lang:all"),
        ],
        [
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="bc_cancel"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
