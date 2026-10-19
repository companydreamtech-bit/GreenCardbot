from aiogram.fsm.state import State, StatesGroup


class AnketaStates(StatesGroup):
    # 1. Asosiy arizachi (Primary Applicant)
    last_name = State()
    first_name = State()
    patronymic = State()
    gender = State()
    birth_date = State()
    birth_place = State()
    education = State()
    address = State()
    phone = State()
    photo = State()
    marital_status = State()

    # 2. Turmush o'rtog'i (Spouse) - agar oilali bo'lsa
    spouse_fullname = State()
    spouse_gender = State()
    spouse_birth_date = State()
    spouse_birth_place = State()
    spouse_education = State()
    spouse_photo = State()

    # 3. Bolalar (Children) - agar 21 yoshgacha bolalari bo'lsa
    children_count = State()
    child_fullname = State()
    child_gender = State()
    child_birth_date = State()
    child_birth_place = State()
    child_photo = State()

    # 4. Yakuniy ko'rib chiqish va tasdiqlash
    review = State()
