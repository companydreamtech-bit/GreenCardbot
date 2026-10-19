import random
import string
from datetime import datetime
from typing import Dict, Any


def generate_application_code() -> str:
    """DV2027-UZ-XXXXXX formatida unikal kod generatsiya qilish"""
    digits = "".join(random.choices(string.digits, k=6))
    return f"DV2027-UZ-{digits}"


def build_admin_report_html(data: Dict[str, Any], app_code: str, user_id: int, username: str = None) -> str:
    """Admin guruhi uchun to'liq va chiroyli HTML hisobot tayyorlash"""
    main = data.get("main", {})
    spouse = data.get("spouse")
    children = data.get("children", [])
    marital = main.get("marital_status", "-")
    tariff = "👨‍👩‍👧‍👦 Oilaviy (149,000 so'm)" if (spouse or len(children) > 0) else "👤 Oddiy (99,000 so'm)"

    user_link = f"@{username}" if username else f"<a href='tg://user?id={user_id}'>Profil</a>"

    html = [
        f"🇺🇸 <b>YANGI DV-2027 ARIZASI!</b>",
        f"━━━━━━━━━━━━━━━━━━",
        f"🆔 <b>Ariza Kodi:</b> <code>{app_code}</code>",
        f"👤 <b>Telegram Foydalanuvchi:</b> {user_link} (ID: <code>{user_id}</code>)",
        f"💎 <b>Tarif:</b> {tariff}",
        f"📅 <b>Qabul qilingan vaqt:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        f"━━━━━━━━━━━━━━━━━━\n",
        f"📋 <b>1. ASOSIY ARIZACHI MA'LUMOTLARI:</b>",
        f"• <b>Familiya:</b> {main.get('last_name', '-')}",
        f"• <b>Ism:</b> {main.get('first_name', '-')}",
        f"• <b>Sharifi (Otasi):</b> {main.get('patronymic', 'Mavjud emas')}",
        f"• <b>Jinsi:</b> {main.get('gender', '-')}",
        f"• <b>Tug'ilgan sana:</b> {main.get('birth_date', '-')}",
        f"• <b>Tug'ilgan joyi:</b> {main.get('birth_place', '-')}",
        f"• <b>Ta'lim darajasi:</b> {main.get('education', '-')}",
        f"• <b>Yashash manzili:</b> {main.get('address', '-')}",
        f"• <b>Telefon raqami:</b> <code>{main.get('phone', '-')}</code>",
        f"• <b>Oilaviy holati:</b> {marital}",
    ]

    if spouse:
        html.extend([
            f"\n💍 <b>2. TURMUSH O'RTOG'I MA'LUMOTLARI:</b>",
            f"• <b>F.I.SH:</b> {spouse.get('fullname', '-')}",
            f"• <b>Jinsi:</b> {spouse.get('gender', '-')}",
            f"• <b>Tug'ilgan sana:</b> {spouse.get('birth_date', '-')}",
            f"• <b>Tug'ilgan joyi:</b> {spouse.get('birth_place', '-')}",
            f"• <b>Ta'lim darajasi:</b> {spouse.get('education', '-')}",
        ])

    if children:
        html.extend([
            f"\n👶 <b>3. 21 YOSHGACHA BO'LGAN BOLALARI ({len(children)} ta):</b>"
        ])
        for idx, child in enumerate(children, 1):
            html.append(
                f"<b>{idx}.</b> {child.get('fullname', '-')} | "
                f"{child.get('gender', '-')} | "
                f"Tug'ilgan: {child.get('birth_date', '-')} | "
                f"Joy: {child.get('birth_place', '-')}"
            )

    html.extend([
        f"\n━━━━━━━━━━━━━━━━━━",
        f"📸 <i>Barcha asl fotosuratlar quyida alohida fayl/hujjat sifatida biriktirilgan.</i>"
    ])

    return "\n".join(html)
