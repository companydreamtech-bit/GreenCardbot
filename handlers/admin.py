import asyncio
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config import config
from database import db
from locales.texts import get_text
from states.admin import AdminStates
from keyboards.inline import get_broadcast_lang_keyboard

logger = logging.getLogger(__name__)
router = Router(name="admin_router")


def is_admin_or_group(user_id: int, chat_id: int) -> bool:
    """Admin yoki admin guruhi ekanligini tekshirish"""
    return (user_id in config.ADMIN_IDS) or (chat_id == config.ADMIN_GROUP_ID)


# =========================================================
# 1. 1-CLICK ACTIONS (ADMIN GURUHIDAN BOSHQARISH)
# =========================================================

# 1.1 To'lovni tasdiqlash
@router.callback_query(F.data.startswith("adm_pay:"))
async def handle_admin_approve_payment(callback: CallbackQuery):
    """Admin to'lovni tasdiqlaganida"""
    if not is_admin_or_group(callback.from_user.id, callback.message.chat.id):
        await callback.answer("⛔ Sizda bu amal uchun ruxsat yo'q!", show_alert=True)
        return

    parts = callback.data.split(":")
    app_code = parts[1]
    target_user_id = int(parts[2])

    await db.update_application_status(app_code, status="paid")
    user_lang = await db.get_user_language(target_user_id)

    # Foydalanuvchiga xabar yuborish
    try:
        await callback.bot.send_message(
            chat_id=target_user_id,
            text=get_text(user_lang, "msg_payment_approved", app_code=app_code),
            parse_mode="HTML",
        )
    except Exception as e:
        logger.warning(f"Could not notify user {target_user_id} about payment: {e}")

    await callback.answer("✅ To'lov tasdiqlandi va foydalanuvchiga xabar berildi!")
    await callback.message.reply(f"💳 <b>{app_code}</b> arizasining to'lovi tasdiqlandi.")


# 1.2 Confirmation Number kiritishni boshlash
@router.callback_query(F.data.startswith("adm_conf:"))
async def handle_admin_start_confirmation(callback: CallbackQuery, state: FSMContext):
    """Admin Confirmation Number kiritish tugmasini bosganda"""
    if not is_admin_or_group(callback.from_user.id, callback.message.chat.id):
        await callback.answer("⛔ Ruxsat yo'q!", show_alert=True)
        return

    parts = callback.data.split(":")
    app_code = parts[1]
    target_user_id = int(parts[2])

    await state.set_state(AdminStates.waiting_conf_number)
    await state.update_data(target_app_code=app_code, target_user_id=target_user_id)

    await callback.answer()
    await callback.message.reply(
        f"📝 <b>{app_code}</b> arizasi uchun rasmiy <b>Confirmation Number</b> ni yuboring:\n"
        f"(Masalan: <code>20271ABCDEF12345</code>)",
        parse_mode="HTML",
    )


# 1.3 Confirmation Number ni qabul qilish va foydalanuvchiga jo'natish
@router.message(AdminStates.waiting_conf_number, F.text)
async def handle_process_confirmation_number(message: Message, state: FSMContext):
    """Admin Confirmation Number kiritganda uni saqlash va arizachiga tantanali yuborish"""
    conf_number = message.text.strip().upper()
    data = await state.get_data()
    app_code = data.get("target_app_code")
    target_user_id = data.get("target_user_id")

    await db.update_application_status(
        app_code, status="approved", confirmation_number=conf_number
    )
    user_lang = await db.get_user_language(target_user_id)

    # Foydalanuvchiga yuborish
    try:
        await message.bot.send_message(
            chat_id=target_user_id,
            text=get_text(
                user_lang,
                "msg_confirmation_issued",
                app_code=app_code,
                conf_number=conf_number,
            ),
            parse_mode="HTML",
        )
        await message.reply(
            f"🎉 <b>{app_code}</b> ga <code>{conf_number}</code> tasdiq kodi biriktirildi va arizachiga yuborildi!",
            parse_mode="HTML",
        )
    except Exception as e:
        await message.reply(f"⚠️ Foydalanuvchiga yuborishda xatolik: {e}")

    await state.clear()


# 1.4 Rad etish (Reject)
@router.callback_query(F.data.startswith("adm_rej:"))
async def handle_admin_start_reject(callback: CallbackQuery, state: FSMContext):
    """Admin arizani rad etishni boshlaganda"""
    if not is_admin_or_group(callback.from_user.id, callback.message.chat.id):
        await callback.answer("⛔ Ruxsat yo'q!", show_alert=True)
        return

    parts = callback.data.split(":")
    app_code = parts[1]
    target_user_id = int(parts[2])

    await state.set_state(AdminStates.waiting_rej_reason)
    await state.update_data(target_app_code=app_code, target_user_id=target_user_id)

    await callback.answer()
    await callback.message.reply(
        f"❌ <b>{app_code}</b> arizasini rad etish sababini yozib yuboring:\n"
        f"(Masalan: <i>Fotosurat talabga javob bermaydi, oq fonda emas</i>)",
        parse_mode="HTML",
    )


@router.message(AdminStates.waiting_rej_reason, F.text)
async def handle_process_rejection_reason(message: Message, state: FSMContext):
    """Rad etish sababini saqlash va foydalanuvchiga yetkazish"""
    reason = message.text.strip()
    data = await state.get_data()
    app_code = data.get("target_app_code")
    target_user_id = data.get("target_user_id")

    await db.update_application_status(
        app_code, status="rejected", rejection_reason=reason
    )
    user_lang = await db.get_user_language(target_user_id)

    try:
        await message.bot.send_message(
            chat_id=target_user_id,
            text=get_text(
                user_lang,
                "msg_application_rejected",
                app_code=app_code,
                reason=reason,
            ),
            parse_mode="HTML",
        )
        await message.reply(
            f"❌ <b>{app_code}</b> rad etildi va foydalanuvchiga sababi bildirildi.",
            parse_mode="HTML",
        )
    except Exception as e:
        await message.reply(f"⚠️ Foydalanuvchiga yuborishda xatolik: {e}")

    await state.clear()


# =========================================================
# 2. BROADCAST (RASSILKA) TIZIMI
# =========================================================
@router.message(Command("broadcast"))
@router.message(Command("send"))
async def handle_start_broadcast(message: Message, state: FSMContext):
    """Rassilka boshlash komandasi"""
    if not (message.from_user.id in config.ADMIN_IDS):
        return

    await state.set_state(AdminStates.waiting_broadcast_content)
    await message.answer(
        "📢 <b>Rassilka (Xabar tarqatish) bo'limi</b>\n\n"
        "Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yuboring (matn, rasm yoki video):",
        parse_mode="HTML",
    )


@router.message(AdminStates.waiting_broadcast_content)
async def handle_broadcast_content(message: Message, state: FSMContext):
    """Rassilka xabarini qabul qilish va til tanlashni so'rash"""
    await state.update_data(
        bc_message_id=message.message_id, bc_chat_id=message.chat.id
    )
    await message.answer(
        "👥 Xabarni qaysi auditoriyaga yubormoqchisiz?",
        reply_markup=get_broadcast_lang_keyboard(),
    )


@router.callback_query(F.data.startswith("bc_lang:"))
async def handle_execute_broadcast(callback: CallbackQuery, state: FSMContext):
    """Xabarni barcha foydalanuvchilarga tarqatish"""
    lang_filter = callback.data.split(":")[1]
    lang = None if lang_filter == "all" else lang_filter

    data = await state.get_data()
    orig_msg_id = data.get("bc_message_id")
    orig_chat_id = data.get("bc_chat_id")

    if not orig_msg_id:
        await callback.answer("Xatolik: Xabar topilmadi.", show_alert=True)
        return

    await callback.answer("🚀 Rassilka boshlandi...")
    status_msg = await callback.message.edit_text("⏳ Xabarlar yuborilmoqda, kuting...")

    users = await db.get_all_users(lang=lang)
    sent_count = 0
    fail_count = 0

    for user in users:
        uid = user["user_id"]
        try:
            await callback.bot.copy_message(
                chat_id=uid,
                from_chat_id=orig_chat_id,
                message_id=orig_msg_id,
            )
            sent_count += 1
            await asyncio.sleep(0.05)  # Telegram limitlariga tushmaslik uchun
        except Exception:
            fail_count += 1

    await status_msg.edit_text(
        f"✅ <b>Rassilka yakunlandi!</b>\n\n"
        f"👥 Jami qamrov: <b>{len(users)}</b> ta\n"
        f"🟢 Muvaffaqiyatli: <b>{sent_count}</b> ta\n"
        f"🔴 Yetkazilmadi / Bloklangan: <b>{fail_count}</b> ta",
        parse_mode="HTML",
    )
    await state.clear()


@router.callback_query(F.data == "bc_cancel")
async def handle_cancel_broadcast(callback: CallbackQuery, state: FSMContext):
    """Rassilkani bekor qilish"""
    await state.clear()
    await callback.message.edit_text("❌ Rassilka bekor qilindi.")


# =========================================================
# 3. STATISTIKA VA TEKSHIRUV
# =========================================================
@router.message(Command("stats"))
@router.message(Command("admin"))
async def handle_admin_stats(message: Message):
    """Adminlar uchun to'liq statistika ko'rsatish"""
    if not (message.from_user.id in config.ADMIN_IDS or message.chat.id == config.ADMIN_GROUP_ID):
        return

    stats = await db.count_stats()
    text = (
        f"📊 <b>Green Card Bot To'liq Statistikasi:</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👥 Jami bot a'zolari: <b>{stats['users_count']}</b> ta\n"
        f"📑 Jami arizalar: <b>{stats['applications_count']}</b> ta\n"
        f"💳 To'langan arizalar: <b>{stats.get('paid_count', 0)}</b> ta\n"
        f"✅ Rasmiy ro'yxatdan o'tganlar: <b>{stats.get('approved_count', 0)}</b> ta\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📢 Yangi e'lon yuborish uchun: <code>/broadcast</code>"
    )
    await message.answer(text, parse_mode="HTML")


@router.message(Command("check"))
async def handle_check_app(message: Message):
    """Ariza kodi bo'yicha qidirish: /check DV2027-UZ-XXXXXX"""
    if not (message.from_user.id in config.ADMIN_IDS or message.chat.id == config.ADMIN_GROUP_ID):
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("ℹ️ Foydalanish: <code>/check DV2027-UZ-XXXXXX</code>", parse_mode="HTML")
        return

    code = parts[1].strip()
    app = await db.get_application_by_code(code)
    if not app:
        await message.answer(f"❌ <code>{code}</code> kodli ariza topilmadi.", parse_mode="HTML")
        return

    main = app["full_data"].get("main", {})
    text = (
        f"🔍 <b>Ariza ma'lumotlari:</b>\n"
        f"🆔 Kod: <code>{app['application_code']}</code>\n"
        f"👤 F.I.SH: <b>{main.get('last_name')} {main.get('first_name')}</b>\n"
        f"📱 Tel: <code>{main.get('phone')}</code>\n"
        f"📌 Status: <b>{app['status']}</b>\n"
        f"📜 Confirmation: <code>{app.get('confirmation_number') or 'Mavjud emas'}</code>\n"
        f"📅 Sana: <b>{app['created_at']}</b>\n"
    )
    await message.answer(text, parse_mode="HTML")
