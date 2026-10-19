import os
import logging
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from config import config
from database import db
from locales.texts import get_text
from states.anketa import AnketaStates
from utils.validators import is_valid_date, is_valid_phone, format_phone, sanitize_name
from utils.helpers import generate_application_code, build_admin_report_html
from utils.pdf_generator import generate_application_pdf
from keyboards.default import (
    get_main_menu_keyboard,
    get_phone_keyboard,
    get_skip_patronymic_keyboard,
    get_cancel_keyboard,
)
from keyboards.inline import (
    get_gender_keyboard,
    get_education_keyboard,
    get_marital_status_keyboard,
    get_children_count_keyboard,
    get_review_keyboard,
    get_admin_user_action_keyboard,
)

logger = logging.getLogger(__name__)
router = Router(name="anketa_router")


async def send_media_to_admin(bot, chat_id: int, file_id: str, caption: str, is_doc: bool = False):
    """Fotosuratni admin guruhiga to'g'ri metod (send_document yoki send_photo) orqali yuborish"""
    try:
        if is_doc:
            await bot.send_document(
                chat_id=chat_id,
                document=file_id,
                caption=caption,
                parse_mode="HTML",
            )
        else:
            await bot.send_photo(
                chat_id=chat_id,
                photo=file_id,
                caption=caption,
                parse_mode="HTML",
            )
    except Exception as e:
        logger.warning(f"Error in primary media send ({e}), trying fallback method...")
        try:
            if is_doc:
                await bot.send_photo(
                    chat_id=chat_id,
                    photo=file_id,
                    caption=caption,
                    parse_mode="HTML",
                )
            else:
                await bot.send_document(
                    chat_id=chat_id,
                    document=file_id,
                    caption=caption,
                    parse_mode="HTML",
                )
        except Exception as err:
            logger.error(f"Fallback media send also failed: {err}")


# =========================================================
# 1. ANKETA BOSHLANISHI
# =========================================================
@router.message(F.text.in_(["📝 Anketa to'ldirish", "📝 Заполнить анкету"]))
async def start_anketa(message: Message, state: FSMContext):
    """Anketa to'ldirish jarayonini boshlash"""
    await state.clear()
    lang = await db.get_user_language(message.from_user.id)
    await state.update_data(lang=lang)

    await state.set_state(AnketaStates.last_name)
    await message.answer(
        text=get_text(lang, "anketa_start"),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML",
    )


# =========================================================
# 2. ASOSIY ARIZACHI MA'LUMOTLARI
# =========================================================
@router.message(AnketaStates.last_name, F.text)
async def process_last_name(message: Message, state: FSMContext):
    """Familiyani qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")

    last_name = sanitize_name(message.text)
    await state.update_data(last_name=last_name)

    await state.set_state(AnketaStates.first_name)
    await message.answer(
        text=get_text(lang, "prompt_firstname"),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML",
    )


@router.message(AnketaStates.first_name, F.text)
async def process_first_name(message: Message, state: FSMContext):
    """Ismni qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")

    first_name = sanitize_name(message.text)
    await state.update_data(first_name=first_name)

    await state.set_state(AnketaStates.patronymic)
    await message.answer(
        text=get_text(lang, "prompt_patronymic"),
        reply_markup=get_skip_patronymic_keyboard(lang),
        parse_mode="HTML",
    )


@router.message(AnketaStates.patronymic, F.text)
async def process_patronymic(message: Message, state: FSMContext):
    """Otasi ismini qabul qilish yoki o'tkazib yuborish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")

    if message.text in [
        get_text(lang, "btn_skip_patronymic"),
        "❌ Mavjud emas (O'tkazib yuborish)",
        "❌ Нет отчества (Пропустить)",
    ]:
        patronymic = ""
    else:
        patronymic = sanitize_name(message.text)

    await state.update_data(patronymic=patronymic)

    await state.set_state(AnketaStates.gender)
    await message.answer(
        text=get_text(lang, "prompt_gender"),
        reply_markup=get_gender_keyboard(lang, prefix="main"),
        parse_mode="HTML",
    )


@router.callback_query(AnketaStates.gender, F.data.startswith("main_gender:"))
async def process_main_gender(callback: CallbackQuery, state: FSMContext):
    """Jinsni qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")
    gender_val = callback.data.split(":")[1]
    gender_text = get_text(lang, "btn_male") if gender_val == "male" else get_text(lang, "btn_female")

    await state.update_data(gender=gender_text)
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        pass

    await state.set_state(AnketaStates.birth_date)
    await callback.message.answer(
        text=get_text(lang, "prompt_birth_date"),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML",
    )


@router.message(AnketaStates.birth_date, F.text)
async def process_birth_date(message: Message, state: FSMContext):
    """Tug'ilgan sanani qabul qilish va tekshirish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")

    if not is_valid_date(message.text):
        await message.answer(
            text=get_text(lang, "error_birth_date"),
            parse_mode="HTML",
        )
        return

    await state.update_data(birth_date=message.text.strip())

    await state.set_state(AnketaStates.birth_place)
    await message.answer(
        text=get_text(lang, "prompt_birth_place"),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML",
    )


@router.message(AnketaStates.birth_place, F.text)
async def process_birth_place(message: Message, state: FSMContext):
    """Tug'ilgan joyini qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")

    await state.update_data(birth_place=message.text.strip())

    await state.set_state(AnketaStates.education)
    await message.answer(
        text=get_text(lang, "prompt_education"),
        reply_markup=get_education_keyboard(lang, prefix="main"),
        parse_mode="HTML",
    )


@router.callback_query(AnketaStates.education, F.data.startswith("main_edu:"))
async def process_main_education(callback: CallbackQuery, state: FSMContext):
    """Ta'lim darajasini qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")
    edu_code = callback.data.split(":")[1]
    edu_text = get_text(lang, f"edu_{edu_code}")

    await state.update_data(education=edu_text)
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        pass

    await state.set_state(AnketaStates.address)
    await callback.message.answer(
        text=get_text(lang, "prompt_address"),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML",
    )


@router.message(AnketaStates.address, F.text)
async def process_address(message: Message, state: FSMContext):
    """Yashash manzilini qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")

    await state.update_data(address=message.text.strip())

    await state.set_state(AnketaStates.phone)
    await message.answer(
        text=get_text(lang, "prompt_phone"),
        reply_markup=get_phone_keyboard(lang),
        parse_mode="HTML",
    )


@router.message(AnketaStates.phone)
async def process_phone(message: Message, state: FSMContext):
    """Telefon raqamni kontakt yoki matn sifatida qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")

    phone = None
    if message.contact:
        phone = message.contact.phone_number
    elif message.text:
        if is_valid_phone(message.text):
            phone = message.text
        else:
            await message.answer(text=get_text(lang, "error_phone"), parse_mode="HTML")
            return

    if not phone:
        await message.answer(text=get_text(lang, "error_phone"), parse_mode="HTML")
        return

    formatted_phone = format_phone(phone)
    await state.update_data(phone=formatted_phone)

    await state.set_state(AnketaStates.photo)
    await message.answer(
        text=get_text(lang, "prompt_photo"),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML",
    )


@router.message(AnketaStates.photo)
async def process_main_photo(message: Message, state: FSMContext):
    """Asosiy arizachi fotosuratini qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")

    file_id = None
    is_doc = False
    if message.photo:
        file_id = message.photo[-1].file_id
        is_doc = False
    elif message.document and (
        message.document.mime_type
        and message.document.mime_type.startswith("image/")
    ):
        file_id = message.document.file_id
        is_doc = True

    if not file_id:
        await message.answer(text=get_text(lang, "error_photo"), parse_mode="HTML")
        return

    await state.update_data(main_photo_id=file_id, main_photo_is_doc=is_doc)

    await state.set_state(AnketaStates.marital_status)
    await message.answer(
        text=get_text(lang, "prompt_marital_status"),
        reply_markup=get_marital_status_keyboard(lang),
        parse_mode="HTML",
    )


# =========================================================
# 3. OILAVIY HOLAT VA TURMUSH O'RTOG'I (SPOUSE)
# =========================================================
@router.callback_query(AnketaStates.marital_status, F.data.startswith("marital:"))
async def process_marital_status(callback: CallbackQuery, state: FSMContext):
    """Oilaviy holatni qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")
    status_code = callback.data.split(":")[1]
    status_text = get_text(lang, f"status_{status_code}")

    await state.update_data(marital_status=status_text, marital_code=status_code)
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        pass

    if status_code == "married":
        # Oilali bo'lsa turmush o'rtog'i ma'lumotlarini so'raymiz
        await state.set_state(AnketaStates.spouse_fullname)
        await callback.message.answer(
            text=f"{get_text(lang, 'spouse_section')}\n\n{get_text(lang, 'spouse_fullname')}",
            reply_markup=get_cancel_keyboard(lang),
            parse_mode="HTML",
        )
    else:
        # Bo'ydoq, ajrashgan yoki beva bo'lsa to'g'ridan-to'g'ri bolalar soniga o'tamiz
        await state.set_state(AnketaStates.children_count)
        await callback.message.answer(
            text=get_text(lang, "prompt_children_count"),
            reply_markup=get_children_count_keyboard(),
            parse_mode="HTML",
        )


@router.message(AnketaStates.spouse_fullname, F.text)
async def process_spouse_fullname(message: Message, state: FSMContext):
    """Turmush o'rtog'ining F.I.SH ini qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")

    await state.update_data(spouse_fullname=sanitize_name(message.text))

    await state.set_state(AnketaStates.spouse_gender)
    await message.answer(
        text=get_text(lang, "spouse_gender"),
        reply_markup=get_gender_keyboard(lang, prefix="spouse"),
        parse_mode="HTML",
    )


@router.callback_query(AnketaStates.spouse_gender, F.data.startswith("spouse_gender:"))
async def process_spouse_gender(callback: CallbackQuery, state: FSMContext):
    """Turmush o'rtog'ining jinsini qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")
    gender_val = callback.data.split(":")[1]
    gender_text = get_text(lang, "btn_male") if gender_val == "male" else get_text(lang, "btn_female")

    await state.update_data(spouse_gender=gender_text)
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        pass

    await state.set_state(AnketaStates.spouse_birth_date)
    await callback.message.answer(
        text=get_text(lang, "spouse_birth_date"),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML",
    )


@router.message(AnketaStates.spouse_birth_date, F.text)
async def process_spouse_birth_date(message: Message, state: FSMContext):
    """Turmush o'rtog'ining tug'ilgan sanasini qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")

    if not is_valid_date(message.text):
        await message.answer(text=get_text(lang, "error_birth_date"), parse_mode="HTML")
        return

    await state.update_data(spouse_birth_date=message.text.strip())

    await state.set_state(AnketaStates.spouse_birth_place)
    await message.answer(
        text=get_text(lang, "spouse_birth_place"),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML",
    )


@router.message(AnketaStates.spouse_birth_place, F.text)
async def process_spouse_birth_place(message: Message, state: FSMContext):
    """Turmush o'rtog'ining tug'ilgan joyini qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")

    await state.update_data(spouse_birth_place=message.text.strip())

    await state.set_state(AnketaStates.spouse_education)
    await message.answer(
        text=get_text(lang, "spouse_education"),
        reply_markup=get_education_keyboard(lang, prefix="spouse"),
        parse_mode="HTML",
    )


@router.callback_query(AnketaStates.spouse_education, F.data.startswith("spouse_edu:"))
async def process_spouse_education(callback: CallbackQuery, state: FSMContext):
    """Turmush o'rtog'ining ta'lim darajasini qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")
    edu_code = callback.data.split(":")[1]
    edu_text = get_text(lang, f"edu_{edu_code}")

    await state.update_data(spouse_education=edu_text)
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        pass

    await state.set_state(AnketaStates.spouse_photo)
    await callback.message.answer(
        text=get_text(lang, "spouse_photo"),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML",
    )


@router.message(AnketaStates.spouse_photo)
async def process_spouse_photo(message: Message, state: FSMContext):
    """Turmush o'rtog'ining fotosuratini qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")

    file_id = None
    is_doc = False
    if message.photo:
        file_id = message.photo[-1].file_id
        is_doc = False
    elif message.document and (
        message.document.mime_type and message.document.mime_type.startswith("image/")
    ):
        file_id = message.document.file_id
        is_doc = True

    if not file_id:
        await message.answer(text=get_text(lang, "error_photo"), parse_mode="HTML")
        return

    await state.update_data(spouse_photo_id=file_id, spouse_photo_is_doc=is_doc)

    # Turmush o'rtog'i tayyor, endi bolalar soniga o'tamiz
    await state.set_state(AnketaStates.children_count)
    await message.answer(
        text=get_text(lang, "prompt_children_count"),
        reply_markup=get_children_count_keyboard(),
        parse_mode="HTML",
    )


# =========================================================
# 4. BOLALAR (CHILDREN) BOSQICHI
# =========================================================
@router.callback_query(AnketaStates.children_count, F.data.startswith("children_count:"))
async def process_children_count(callback: CallbackQuery, state: FSMContext):
    """Bolalar sonini qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")
    count = int(callback.data.split(":")[1])

    await state.update_data(children_target=count, children_list=[], current_child_index=1)
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        pass

    if count == 0:
        # Bolalar yo'q bo'lsa darhol ko'rib chiqishga o'tamiz
        await show_review(callback.message, state)
    else:
        # 1-bola ma'lumotlarini so'raymiz
        await state.set_state(AnketaStates.child_fullname)
        await callback.message.answer(
            text=f"{get_text(lang, 'child_section', index=1)}\n\n{get_text(lang, 'child_fullname', index=1)}",
            reply_markup=get_cancel_keyboard(lang),
            parse_mode="HTML",
        )


@router.message(AnketaStates.child_fullname, F.text)
async def process_child_fullname(message: Message, state: FSMContext):
    """Bola F.I.SH ini qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")
    idx = data.get("current_child_index", 1)

    await state.update_data(temp_child_fullname=sanitize_name(message.text))

    await state.set_state(AnketaStates.child_gender)
    await message.answer(
        text=get_text(lang, "child_gender"),
        reply_markup=get_gender_keyboard(lang, prefix="child"),
        parse_mode="HTML",
    )


@router.callback_query(AnketaStates.child_gender, F.data.startswith("child_gender:"))
async def process_child_gender(callback: CallbackQuery, state: FSMContext):
    """Bola jinsini qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")
    idx = data.get("current_child_index", 1)
    gender_val = callback.data.split(":")[1]
    gender_text = get_text(lang, "btn_male") if gender_val == "male" else get_text(lang, "btn_female")

    await state.update_data(temp_child_gender=gender_text)
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        pass

    await state.set_state(AnketaStates.child_birth_date)
    await callback.message.answer(
        text=get_text(lang, "child_birth_date", index=idx),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML",
    )


@router.message(AnketaStates.child_birth_date, F.text)
async def process_child_birth_date(message: Message, state: FSMContext):
    """Bola tug'ilgan sanasini qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")
    idx = data.get("current_child_index", 1)

    if not is_valid_date(message.text):
        await message.answer(text=get_text(lang, "error_birth_date"), parse_mode="HTML")
        return

    await state.update_data(temp_child_birth_date=message.text.strip())

    await state.set_state(AnketaStates.child_birth_place)
    await message.answer(
        text=get_text(lang, "child_birth_place", index=idx),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML",
    )


@router.message(AnketaStates.child_birth_place, F.text)
async def process_child_birth_place(message: Message, state: FSMContext):
    """Bola tug'ilgan joyini qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")
    idx = data.get("current_child_index", 1)

    await state.update_data(temp_child_birth_place=message.text.strip())

    await state.set_state(AnketaStates.child_photo)
    await message.answer(
        text=get_text(lang, "child_photo", index=idx),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML",
    )


@router.message(AnketaStates.child_photo)
async def process_child_photo(message: Message, state: FSMContext):
    """Bola fotosuratini qabul qilish va keyingi bolaga o'tish yoki yakunlash"""
    data = await state.get_data()
    lang = data.get("lang", "uz")
    idx = data.get("current_child_index", 1)
    target = data.get("children_target", 0)
    children_list = data.get("children_list", [])

    file_id = None
    is_doc = False
    if message.photo:
        file_id = message.photo[-1].file_id
        is_doc = False
    elif message.document and (
        message.document.mime_type and message.document.mime_type.startswith("image/")
    ):
        file_id = message.document.file_id
        is_doc = True

    if not file_id:
        await message.answer(text=get_text(lang, "error_photo"), parse_mode="HTML")
        return

    # Bolani saqlaymiz
    child_info = {
        "fullname": data.get("temp_child_fullname"),
        "gender": data.get("temp_child_gender"),
        "birth_date": data.get("temp_child_birth_date"),
        "birth_place": data.get("temp_child_birth_place"),
        "photo_id": file_id,
        "is_doc": is_doc,
    }
    children_list.append(child_info)
    await state.update_data(children_list=children_list)

    if idx < target:
        # Keyingi bolaga o'tish
        next_idx = idx + 1
        await state.update_data(current_child_index=next_idx)
        await state.set_state(AnketaStates.child_fullname)
        await message.answer(
            text=f"{get_text(lang, 'child_section', index=next_idx)}\n\n{get_text(lang, 'child_fullname', index=next_idx)}",
            reply_markup=get_cancel_keyboard(lang),
            parse_mode="HTML",
        )
    else:
        # Barcha bolalar to'ldirildi -> Review ga o'tamiz
        await show_review(message, state)


# =========================================================
# 5. REVIEW (KO'RIB CHIQISH VA TASDIQLASH)
# =========================================================
async def show_review(target_obj: Message, state: FSMContext):
    """Foydalanuvchiga barcha to'plangan ma'lumotlarni ko'rib chiqish uchun chiqarish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")

    review_text = get_text(lang, "review_title")
    review_text += get_text(
        lang,
        "review_main_applicant",
        last_name=data.get("last_name", "-"),
        first_name=data.get("first_name", "-"),
        patronymic=data.get("patronymic", "-"),
        gender=data.get("gender", "-"),
        birth_date=data.get("birth_date", "-"),
        birth_place=data.get("birth_place", "-"),
        education=data.get("education", "-"),
        address=data.get("address", "-"),
        phone=data.get("phone", "-"),
        marital_status=data.get("marital_status", "-"),
    )

    if data.get("marital_code") == "married":
        review_text += get_text(
            lang,
            "review_spouse",
            fullname=data.get("spouse_fullname", "-"),
            gender=data.get("spouse_gender", "-"),
            birth_date=data.get("spouse_birth_date", "-"),
            birth_place=data.get("spouse_birth_place", "-"),
            education=data.get("spouse_education", "-"),
        )

    children = data.get("children_list", [])
    if children:
        review_text += get_text(lang, "review_children_header", count=len(children))
        for i, child in enumerate(children, 1):
            review_text += get_text(
                lang,
                "review_child_item",
                index=i,
                fullname=child.get("fullname", "-"),
                gender=child.get("gender", "-"),
                birth_date=child.get("birth_date", "-"),
                birth_place=child.get("birth_place", "-"),
            )

    await state.set_state(AnketaStates.review)
    await target_obj.answer(
        text=review_text,
        reply_markup=get_review_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(AnketaStates.review, F.data == "review:restart")
async def handle_review_restart(callback: CallbackQuery, state: FSMContext):
    """Qayta to'ldirish tugmasi"""
    data = await state.get_data()
    lang = data.get("lang", "uz")
    await state.clear()
    await state.update_data(lang=lang)

    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        pass

    await state.set_state(AnketaStates.last_name)
    await callback.message.answer(
        text=get_text(lang, "anketa_start"),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(AnketaStates.review, F.data == "review:confirm")
async def handle_review_confirm(callback: CallbackQuery, state: FSMContext):
    """Arizani tasdiqlash va Admin guruhiga jo'natish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")
    user_id = callback.from_user.id
    username = callback.from_user.username
    full_name = f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()

    await callback.answer("⏳ Arizangiz qabul qilinmoqda...")

    try:
        await callback.message.delete()
    except Exception:
        pass

    # 1. Unikal ariza kodini generatsiya qilish
    app_code = generate_application_code()

    # 2. Ma'lumotlarni strukturaviy JSON formatga yig'ish
    structured_data = {
        "application_code": app_code,
        "user_id": user_id,
        "username": username,
        "language": lang,
        "created_at": datetime.now().isoformat(),
        "main": {
            "last_name": data.get("last_name"),
            "first_name": data.get("first_name"),
            "patronymic": data.get("patronymic"),
            "gender": data.get("gender"),
            "birth_date": data.get("birth_date"),
            "birth_place": data.get("birth_place"),
            "education": data.get("education"),
            "address": data.get("address"),
            "phone": data.get("phone"),
            "marital_status": data.get("marital_status"),
            "marital_code": data.get("marital_code"),
            "photo_id": data.get("main_photo_id"),
        },
        "spouse": None,
        "children": data.get("children_list", []),
    }

    if data.get("marital_code") == "married":
        structured_data["spouse"] = {
            "fullname": data.get("spouse_fullname"),
            "gender": data.get("spouse_gender"),
            "birth_date": data.get("spouse_birth_date"),
            "birth_place": data.get("spouse_birth_place"),
            "education": data.get("spouse_education"),
            "photo_id": data.get("spouse_photo_id"),
        }

    # 3. Ma'lumotlar bazasiga saqlash
    try:
        await db.save_application(
            application_code=app_code,
            user_id=user_id,
            full_data=structured_data,
            status="submitted",
        )
    except Exception as e:
        logger.error(f"Error saving application to DB: {e}")

    # 4. Admin guruhiga hisobot yuborish
    try:
        admin_report_text = build_admin_report_html(
            data=structured_data,
            app_code=app_code,
            user_id=user_id,
            username=username,
        )
        admin_markup = get_admin_user_action_keyboard(
            app_code=app_code,
            user_id=user_id,
            username=username,
            phone=data.get("phone"),
        )
        # Guruhga matn yuborish
        await callback.bot.send_message(
            chat_id=config.ADMIN_GROUP_ID,
            text=admin_report_text,
            reply_markup=admin_markup,
            parse_mode="HTML",
        )

        # PDF hujjatini yaratish va adminga uzatish
        pdf_path = f"app_{app_code}.pdf"
        try:
            generate_application_pdf(data=structured_data, app_code=app_code, output_path=pdf_path)
            await callback.bot.send_document(
                chat_id=config.ADMIN_GROUP_ID,
                document=FSInputFile(pdf_path),
                caption=f"📄 <b>Rasmiy PDF Anketa Varaqasi:</b> <code>{app_code}</code>",
                parse_mode="HTML",
            )
        except Exception as e:
            logger.error(f"Error generating/sending PDF to admin: {e}")

        # 5. Fotosuratlarni admin guruhiga to'g'ri jo'natish
        # Asosiy arizachi surati
        main_photo_id = data.get("main_photo_id")
        main_is_doc = data.get("main_photo_is_doc", False)
        if main_photo_id:
            await send_media_to_admin(
                bot=callback.bot,
                chat_id=config.ADMIN_GROUP_ID,
                file_id=main_photo_id,
                caption=f"📸 <b>Asosiy arizachi fotosurati (5x5):</b>\n👤 {full_name}\n🆔 Ariza: <code>{app_code}</code>",
                is_doc=main_is_doc,
            )

        # Turmush o'rtog'i surati
        if structured_data.get("spouse") and structured_data["spouse"].get("photo_id"):
            spouse_photo_id = structured_data["spouse"]["photo_id"]
            spouse_is_doc = data.get("spouse_photo_is_doc", False)
            await send_media_to_admin(
                bot=callback.bot,
                chat_id=config.ADMIN_GROUP_ID,
                file_id=spouse_photo_id,
                caption=f"💍 <b>Turmush o'rtog'i fotosurati (5x5):</b>\n👤 {structured_data['spouse']['fullname']}\n🆔 Ariza: <code>{app_code}</code>",
                is_doc=spouse_is_doc,
            )

        # Bolalar suratlari
        for i, child in enumerate(structured_data.get("children", []), 1):
            if child.get("photo_id"):
                await send_media_to_admin(
                    bot=callback.bot,
                    chat_id=config.ADMIN_GROUP_ID,
                    file_id=child["photo_id"],
                    caption=f"👶 <b>{i}-farzand fotosurati (5x5):</b>\n👤 {child['fullname']}\n🆔 Ariza: <code>{app_code}</code>",
                    is_doc=child.get("is_doc", False),
                )

    except Exception as e:
        logger.error(f"Error forwarding application to admin group: {e}", exc_info=True)

    # 6. Foydalanuvchiga muvaffaqiyat xabari va to'lov rekvizitlari
    is_family = bool(structured_data.get("spouse") or len(structured_data.get("children", [])) > 0)
    tariff_name = (
        "👨‍👩‍👧‍👦 Oilaviy tarif" if (lang == "uz" and is_family)
        else "👤 Oddiy tarif" if lang == "uz"
        else "👨‍👩‍👧‍👦 Семейный тариф" if is_family
        else "👤 Одиночный тариф"
    )
    tariff_price = "149,000 so'm" if (is_family and lang == "uz") else "99,000 so'm" if lang == "uz" else "149,000 сум" if is_family else "99,000 сум"

    success_msg = get_text(
        lang,
        "success_submission",
        app_code=app_code,
        full_name=full_name,
        created_at=datetime.now().strftime("%d.%m.%Y %H:%M"),
        tariff_name=tariff_name,
        tariff_price=tariff_price,
        card_number=config.PAYMENT_CARD_NUMBER,
        card_holder=config.PAYMENT_CARD_HOLDER,
        channel=config.CHANNEL_USERNAME,
    )

    await state.clear()

    await callback.message.answer(
        text=success_msg,
        reply_markup=get_main_menu_keyboard(lang),
        parse_mode="HTML",
    )

    # Foydalanuvchiga ham PDF nusxasini jo'natish
    pdf_user_path = f"app_{app_code}.pdf"
    if os.path.exists(pdf_user_path):
        try:
            await callback.message.answer_document(
                document=FSInputFile(pdf_user_path),
                caption=f"📄 <b>{app_code}</b> — Green Card DV-2027 rasmiy anketa varaqangiz (PDF)",
                parse_mode="HTML",
            )
        except Exception as e:
            logger.error(f"Error sending PDF to user: {e}")
        finally:
            try:
                os.remove(pdf_user_path)
            except Exception:
                pass


# =========================================================
# 6. TO'LOV CHEKINI QABUL QILISH (FSM TASHQARISIDA)
# =========================================================
@router.message(F.photo | (F.document & F.document.mime_type.startswith("image/")))
async def handle_payment_receipt(message: Message, state: FSMContext):
    """Foydalanuvchi to'lov chekini yuborganida uni admin guruhiga yetkazish"""
    current_state = await state.get_state()
    if current_state is not None:
        return

    lang = await db.get_user_language(message.from_user.id)
    user_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else f"ID: {user_id}"

    caption = (
        f"🧾 <b>YANGI TO'LOV CHEKI / SKRINSHOT!</b>\n"
        f"👤 Foydalanuvchi: {username} (<code>{user_id}</code>)\n"
        f"📅 Sana: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )

    try:
        if message.photo:
            await message.bot.send_photo(
                chat_id=config.ADMIN_GROUP_ID,
                photo=message.photo[-1].file_id,
                caption=caption,
                parse_mode="HTML",
            )
        elif message.document:
            await message.bot.send_document(
                chat_id=config.ADMIN_GROUP_ID,
                document=message.document.file_id,
                caption=caption,
                parse_mode="HTML",
            )

        reply_text = (
            "✅ <b>To'lov chekingiz adminga yetkazildi!</b>\n"
            "Tez orada arizangiz tekshirilib, tasdiq kodi (Confirmation Number) taqdim etiladi."
            if lang == "uz"
            else "✅ <b>Чек об оплате передан администратору!</b>\n"
            "В ближайшее время ваша анкета будет проверена и вам будет выдан код подтверждения."
        )
        await message.answer(reply_text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error forwarding payment receipt: {e}")

