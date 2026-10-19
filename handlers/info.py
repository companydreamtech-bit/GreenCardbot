from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database import db
from locales.texts import get_text
from keyboards.default import get_main_menu_keyboard
from config import config

router = Router(name="info_router")


@router.message(F.text.in_(["🔍 Arizam holati", "🔍 Статус заявки"]))
async def handle_my_status(message: Message):
    """Foydalanuvchi arizalari holatini ko'rsatish"""
    lang = await db.get_user_language(message.from_user.id)
    apps = await db.get_user_applications(message.from_user.id)

    if not apps:
        await message.answer(get_text(lang, "status_empty"), parse_mode="HTML")
        return

    text = get_text(lang, "status_title")
    for app in apps:
        st = app.get("status", "submitted")
        badge = get_text(lang, f"badge_{st}")

        details = ""
        if st == "approved" and app.get("confirmation_number"):
            details = (
                f"\n📜 <b>Confirmation Number:</b> <code>{app['confirmation_number']}</code>"
            )
        elif st == "rejected" and app.get("rejection_reason"):
            details = f"\n⚠️ <b>Izoh:</b> {app['rejection_reason']}"

        main_info = app.get("full_data", {}).get("main", {})
        name = f"{main_info.get('first_name', '')} {main_info.get('last_name', '')}".strip()

        created_at = app.get("created_at", "-")
        if "T" in str(created_at):
            created_at = str(created_at).replace("T", " ")[:16]

        text += get_text(
            lang,
            "status_item",
            app_code=app.get("application_code"),
            name=name,
            status_badge=badge,
            created_at=created_at,
            details=details,
        )

    await message.answer(text, parse_mode="HTML")


@router.message(F.text.in_(["👥 Do'stlarni taklif qilish", "👥 Пригласить друзей"]))
async def handle_referral(message: Message):
    """Referal bo'limi va statistikasini ko'rsatish"""
    lang = await db.get_user_language(message.from_user.id)
    user_id = message.from_user.id

    bot_info = await message.bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start=ref_{user_id}"

    stats = await db.get_referral_stats(user_id)
    text = get_text(
        lang,
        "referral_info",
        ref_link=ref_link,
        invited=stats["invited_count"],
        applied=stats["applied_count"],
        discount=stats["discount_sum"],
    )
    await message.answer(text, parse_mode="HTML")


@router.message(F.text.in_(["📸 Fotosurat talablari", "📸 Требования к фото"]))
async def handle_photo_rules(message: Message):
    """Fotosurat talablarini ko'rsatish"""
    lang = await db.get_user_language(message.from_user.id)
    text = get_text(lang, "photo_rules")
    await message.answer(text, parse_mode="HTML")


@router.message(F.text.in_(["💰 Tariflar va To'lov", "💰 Тарифы и оплаta"]))
@router.message(F.text.in_(["💰 Tariflar va To'lov", "💰 Тарифы и оплата"]))
async def handle_pricing(message: Message):
    """Tariflar va to'lov rekvizitlarini ko'rsatish"""
    lang = await db.get_user_language(message.from_user.id)
    text = get_text(
        lang,
        "pricing",
        card_number=config.PAYMENT_CARD_NUMBER,
        card_holder=config.PAYMENT_CARD_HOLDER,
        phone=config.PAYMENT_PHONE,
    )
    await message.answer(text, parse_mode="HTML")


@router.message(F.text.in_(["❓ Ko'p beriladigan savollar", "❓ Частые вопросы (FAQ)", "❓ Частые вопросы"]))
async def handle_faq(message: Message):
    """FAQ bo'limini ko'rsatish"""
    lang = await db.get_user_language(message.from_user.id)
    text = get_text(lang, "faq")
    await message.answer(text, parse_mode="HTML")


@router.message(F.text.in_(["❌ Bekor qilish", "❌ Отмена"]))
async def handle_cancel(message: Message, state: FSMContext):
    """FSM jarayonini bekor qilish"""
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
    lang = await db.get_user_language(message.from_user.id)
    await message.answer(
        text=get_text(lang, "cancelled"),
        reply_markup=get_main_menu_keyboard(lang),
        parse_mode="HTML",
    )
