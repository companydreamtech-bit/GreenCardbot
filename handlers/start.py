from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from database import db
from locales.texts import get_text
from keyboards.default import get_main_menu_keyboard
from keyboards.inline import get_language_keyboard

router = Router(name="start_router")


@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext):
    """Start komandasi va referal qayta ishlovchisi"""
    await state.clear()
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name

    # Referal parametrini ajratib olish (masalan /start ref_12345)
    referrer_id = None
    args = message.text.split()
    if len(args) > 1 and args[1].startswith("ref_"):
        raw_ref = args[1].replace("ref_", "")
        if raw_ref.isdigit() and int(raw_ref) != user_id:
            referrer_id = int(raw_ref)

    user = await db.get_user(user_id)
    if not user:
        # Yangi foydalanuvchini bazaga qo'shish (referal bilan)
        await db.add_or_update_user(
            user_id=user_id,
            username=username,
            full_name=full_name,
            language="uz",
            referrer_id=referrer_id,
        )
        await message.answer(
            text=get_text("uz", "choose_language"),
            reply_markup=get_language_keyboard(),
            parse_mode="HTML",
        )
    else:
        # Mavjud foydalanuvchiga asosiy menyuni ko'rsatish
        lang = user.get("language", "uz")
        await message.answer(
            text=get_text(lang, "main_menu"),
            reply_markup=get_main_menu_keyboard(lang),
            parse_mode="HTML",
        )


@router.message(F.text.in_(["🌐 Tilni o'zgartirish", "🌐 Сменить язык"]))
@router.message(Command("lang"))
async def handle_change_language(message: Message, state: FSMContext):
    """Tilni o'zgartirish menyusi"""
    await state.clear()
    lang = await db.get_user_language(message.from_user.id)
    await message.answer(
        text=get_text(lang, "choose_language"),
        reply_markup=get_language_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("set_lang:"))
async def handle_set_language_callback(callback: CallbackQuery, state: FSMContext):
    """Til tanlanganda qayta ishlash"""
    lang = callback.data.split(":")[1]
    user_id = callback.from_user.id
    username = callback.from_user.username
    full_name = callback.from_user.full_name

    await db.add_or_update_user(
        user_id=user_id, username=username, full_name=full_name, language=lang
    )
    await callback.answer(get_text(lang, "lang_selected"))

    try:
        await callback.message.delete()
    except Exception:
        pass

    await callback.message.answer(
        text=get_text(lang, "main_menu"),
        reply_markup=get_main_menu_keyboard(lang),
        parse_mode="HTML",
    )
