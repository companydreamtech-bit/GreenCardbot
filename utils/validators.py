import re
from datetime import datetime
from typing import Optional


def is_valid_date(date_text: str) -> bool:
    """Sana DD.MM.YYYY formatida va to'g'ri oraliqda ekanini tekshirish"""
    date_text = date_text.strip()
    match = re.match(r"^(\d{2})[./\-](\d{2})[./\-](\d{4})$", date_text)
    if not match:
        return False
    
    day, month, year = int(match.group(1)), int(match.group(2)), int(match.group(3))
    try:
        dt = datetime(year, month, day)
        current_year = datetime.now().year
        # Green Card uchun tug'ilgan yil 1920 dan joriy yilgacha bo'lishi lozim
        if 1920 <= year <= current_year and dt <= datetime.now():
            return True
    except ValueError:
        return False
    return False


def is_valid_phone(phone_text: str) -> bool:
    """Telefon raqam to'g'riligini tekshirish (masalan: +998901234567 yoki 998901234567)"""
    cleaned = re.sub(r"[\s\-\(\)]", "", phone_text)
    match = re.match(r"^\+?\d{9,15}$", cleaned)
    return bool(match)


def format_phone(phone_text: str) -> str:
    """Telefon raqamni toza xalqaro formatga keltirish"""
    cleaned = re.sub(r"[\s\-\(\)]", "", phone_text)
    if not cleaned.startswith("+"):
        cleaned = "+" + cleaned
    return cleaned


def sanitize_name(text: str) -> str:
    """Ism, familiya va otasining ismini tozalash va to'g'rilash"""
    return text.strip().title()
