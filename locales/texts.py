from typing import Dict, Any

TEXTS: Dict[str, Dict[str, Any]] = {
    "uz": {
        # Start & Language
        "choose_language": "🇺🇿 <b>Assalomu alaykum!</b>\nGreen Card DV-2027 rasmiy ro'yxatdan o'tish botiga xush kelibsiz.\n\nIltimos, o'zingizga qulay tilni tanlang:\n\n---\n\n🇷🇺 <b>Здравствуйте!</b>\nДобро пожаловать в официальный бот регистрации Green Card DV-2027.\n\nПожалуйста, выберите удобный язык:",
        "lang_selected": "✅ O'zbek tili tanlandi!",
        "lang_changed": "✅ Til muvaffaqiyatli o'zgartirildi!",
        
        # Main Menu Buttons
        "btn_anketa": "📝 Anketa to'ldirish",
        "btn_website": "🌐 Veb-saytda to'ldirish",
        "btn_photo_rules": "📸 Fotosurat talablari",
        "btn_pricing": "💰 Tariflar va To'lov",
        "btn_faq": "❓ Ko'p beriladigan savollar",
        "btn_my_status": "🔍 Arizam holati",
        "btn_referral": "👥 Do'stlarni taklif qilish",
        "btn_change_lang": "🌐 Tilni o'zgartirish",
        "btn_cancel": "❌ Bekor qilish",
        "btn_skip_patronymic": "❌ Mavjud emas (O'tkazib yuborish)",
        "btn_send_contact": "📱 Telefon raqamni yuborish",

        # Main Menu Welcome
        "main_menu": (
            "🏛 <b>AQSh Green Card DV-2027 Dasturi</b>\n\n"
            "Quyidagi bo'limlardan birini tanlang:\n\n"
            "• 📝 <b>Anketa to'ldirish</b> — Bot orqali arizani bosqichma-bosqich jo'natish.\n"
            "• 🌐 <b>Veb-saytda to'ldirish</b> — Rasmiy veb-ilovamiz orqali to'ldirish.\n"
            "• 🔍 <b>Arizam holati</b> — Yuborilgan arizangiz tekshiruvi va tasdiq kodi.\n"
            "• 👥 <b>Do'stlarni taklif qilish</b> — Har bir do'stingiz uchun 20,000 so'm chegirma!\n"
            "• 📸 <b>Fotosurat talablari</b> — 5x5 sm rasmlar bo'yicha qo'llanma.\n"
            "• 💰 <b>Tariflar va To'lov</b> — Xizmat narxlari va to'lov usullari.\n"
            "• ❓ <b>Ko'p beriladigan savollar</b> — Muhim qoidalar va eslatmalar."
        ),

        # Status Checker
        "status_empty": "ℹ️ <b>Sizda hali yuborilgan arizalar mavjud emas.</b>\nAriza topshirish uchun 📝 <b>Anketa to'ldirish</b> tugmasini bosing.",
        "status_title": "📋 <b>Sizning arizalaringiz holati:</b>\n\n",
        "status_item": (
            "🆔 <b>Ariza Kodi:</b> <code>{app_code}</code>\n"
            "👤 <b>Arizachi:</b> {name}\n"
            "📌 <b>Holat:</b> {status_badge}\n"
            "📅 <b>Sana:</b> {created_at}\n"
            "{details}\n"
            "━━━━━━━━━━━━━━━━━━\n"
        ),
        "badge_submitted": "⏳ <b>Tekshirilmoqda / To'lov kutilmoqda</b>",
        "badge_paid": "💳 <b>To'lov qabul qilindi / Tizimga kiritilmoqda</b>",
        "badge_approved": "✅ <b>RASMIY RO'YXATDAN O'TDI!</b>",
        "badge_rejected": "❌ <b>Qayta to'ldirish talab etiladi</b>",

        # Referral System
        "referral_info": (
            "👥 <b>Do'stlaringizni taklif qiling va chegirmaga ega bo'ling!</b>\n\n"
            "Sizning shaxsiy referal havolangiz:\n"
            "👉 <code>{ref_link}</code>\n\n"
            "💡 <b>Shartlar:</b>\n"
            "Ushbu havola orqali botga kirib ariza topshirgan har bir do'stingiz uchun sizga <b>20,000 so'm</b> chegirma / bonus taqdim etiladi!\n\n"
            "📊 <b>Sizning statistikangiz:</b>\n"
            "• Taklif qilingan do'stlar: <b>{invited}</b> ta\n"
            "• Ariza topshirganlar: <b>{applied}</b> ta\n"
            "• Sizning jami chegirmangiz: <b>{discount:,} so'm</b>"
        ),

        # Photo Requirements
        "photo_rules": (
            "📸 <b>AQSh Green Card (DV-Lotereya) Fotosurat Talablari</b>\n\n"
            "Anketangiz qabul qilinishi uchun fotosurat AQSh Davlat Departamenti talablariga 100% mos kelishi shart:\n\n"
            "1. <b>Hajmi va o'lchami:</b> 600x600 piksel (5x5 sm), kvadrat shaklda.\n"
            "2. <b>Foni:</b> Bir tekis oq yoki och oq fonda bo'lishi kerak. Hech qanday soya yoki naqsh bo'lmasligi shart.\n"
            "3. <b>Yuz holati:</b> Kamera markazida, to'g'riga qaragan, neytral mimika (tabassum qilmasdan, ko'zlar ochiq).\n"
            "4. <b>Ko'zoynak va bosh kiyim:</b> Ko'zoynak taqish qat'iyan man etiladi! Diniy sababli ro'mol o'raganda ham yuz peshonadan iyakgacha to'liq ochiq ko'rinishi shart.\n"
            "5. <b>Yangi olingan bo'lishi:</b> Oxirgi 6 oy ichida olingan yangi rasm bo'lishi shart.\n"
            "6. <b>Sifati:</b> Retush, filtr (Photoshop) yoki yuzni o'zgartiruvchi sun'iy intellekt ishlatilmagan bo'lishi zarur.\n\n"
            "<i>💡 Rasm yuborishda sifat buzilmasligi uchun fayl (Hujjat/Document) shaklida yuborish tavsiya etiladi.</i>"
        ),

        # Pricing & Payment
        "pricing": (
            "💰 <b>Xizmat Tariflari va To'lov Rekvizitlari</b>\n\n"
            "Biz anketangizni xatolarsiz, AQSh Davlat Departamenti qoidalariga to'liq mos ravishda rasmiy tizimga kiritib, tasdiq kodini (Confirmation Number) taqdim etamiz.\n\n"
            "💵 <b>Tariflar:</b>\n"
            "• 👤 <b>Oddiy (Yakka tartibda):</b> 99,000 so'm\n"
            "• 👨‍👩‍👧‍👦 <b>Oilaviy (Er-xotin va bolalar):</b> 149,000 so'm\n\n"
            "💳 <b>To'lov usullari (Click / Payme):</b>\n"
            "Karta: <code>{card_number}</code>\n"
            "Egasi: <b>{card_holder}</b>\n"
            "Telefon: <b>{phone}</b>\n\n"
            "<i>⚠️ To'lov chekini anketani tasdiqlaganingizdan so'ng adminga yuborishingiz mumkin.</i>"
        ),

        # FAQ
        "faq": (
            "❓ <b>Ko'p Beriladigan Savollar (FAQ)</b>\n\n"
            "<b>1. Green Card nima beradi?</b>\n"
            "AQShda doimiy yashash, qonuniy ishlash, ta'lim olish va 5 yildan so'ng AQSh fuqaroligini olish huquqini beradi.\n\n"
            "<b>2. Kimlar qatnasha oladi?</b>\n"
            "O'rta maktab (11-sinf) yoki kollej/litseyni tamomlagan O'zbekiston fuqarolari.\n\n"
            "<b>3. Ingliz tilini bilish shartmi?</b>\n"
            "Yo'q, dastlab ariza topshirishda ingliz tili darajasi talab etilmaydi.\n\n"
            "<b>4. Pasport muddati tugagan bo'lsa-chi?</b>\n"
            "Arizani ID karta yoki amaldagi xorijga chiqish (qizil) pasporti ma'lumotlari bilan to'ldirishingiz mumkin.\n\n"
            "<b>5. Natijalar qachon chiqadi?</b>\n"
            "Natijalar may oyining boshida AQSh rasmiy saytida e'lon qilinadi."
        ),

        # Anketa FSM Prompts
        "anketa_start": "📝 <b>Green Card DV-2027 Anketasini to'ldirish</b>\n\nIltimos, barcha ma'lumotlarni <b>ingliz (lotin) harflarida</b>, xorijga chiqish pasportingiz yoki ID-kartangizdagidek to'g'ri kiriting.\n\nIstalgan vaqtda bekor qilish uchun '❌ Bekor qilish' tugmasini bosishingiz mumkin.\n\n<b>1-qadam:</b> Familiyangizni kiriting (Masalan: <code>Valiyev</code> yoki <code>Karimova</code>):",
        "prompt_firstname": "<b>2-qadam:</b> Ismingizni kiriting (Masalan: <code>Alisher</code> yoki <code>Madina</code>):",
        "prompt_patronymic": "<b>3-qadam:</b> Otangizning ismini kiriting (Lotin harflarida, masalan: <code>Rustamovich</code>).\nAgar otangizning ismi pasportingizda bo'lmasa, quyidagi tugmani bosing:",
        "prompt_gender": "<b>4-qadam:</b> Jinsingizni tanlang:",
        "btn_male": "👨 Erkak",
        "btn_female": "👩 Ayol",
        "prompt_birth_date": "<b>5-qadam:</b> Tug'ilgan sanangizni kiriting.\nFormat: <code>KK.OO.YYYY</code> (Masalan: <code>15.04.1995</code>):",
        "error_birth_date": "⚠️ <b>Noto'g'ri sana formati!</b>\nIltimos, sanani <code>KK.OO.YYYY</code> ko'rinishida kiriting (Masalan: <code>24.11.1998</code>) va haqiqiy sanani kiriting:",
        "prompt_birth_place": "<b>6-qadam:</b> Tug'ilgan mamlakat va shahar/tumaningizni kiriting:\n(Masalan: <code>O'zbekiston, Toshkent shahar</code> yoki <code>Uzbekistan, Samarqand</code>):",
        "prompt_education": "<b>7-qadam:</b> Ta'lim darajangizni tanlang:",
        "edu_primary": "🏫 O'rta maktab (11-sinf)",
        "edu_college": "🎓 Kollej / Litsey / Texnikum",
        "edu_bachelor": "🏛 Oliy ta'lim (Bakalavr)",
        "edu_master": "📚 Magistratura / Fan nomzodi",
        "prompt_address": "<b>8-qadam:</b> Hozirgi doimiy yashash manzilingizni kiriting:\n(Masalan: <code>Toshkent sh., Chilonzor tumani, 9-mavze, 12-uy, 45-xonadon</code>):",
        "prompt_phone": "<b>9-qadam:</b> Telefon raqamingizni yuboring:\nPastdagi tugmani bosing yoki <code>+998901234567</code> formatida yozing:",
        "error_phone": "⚠️ <b>Noto'g'ri telefon raqami!</b>\nIltimos, pastdagi '📱 Telefon raqamni yuborish' tugmasini bosing yoki to'g'ri xalqaro formatda kiriting (Masalan: <code>+998901234567</code>):",
        "prompt_photo": "<b>10-qadam:</b> 📸 <b>Asosiy arizachining fotosuratini yuboring.</b>\n\n• Surat 5x5 sm (600x600 px) oq fonda bo'lishi kerak.\n• Ko'zoynaksiz bo'lishi shart.\n• Sifat yo'qolmasligi uchun fayl (Hujjat/Document) ko'rinishida yoki sifatli rasm tarzida yuboring:",
        "error_photo": "⚠️ Iltimos, faqat rasm yoki fotosurat faylini (JPG/PNG/JPEG) yuboring!",
        "prompt_marital_status": "<b>11-qadam:</b> Oilaviy holatingizni tanlang:",
        "status_single": "👤 Bo'ydoq / Turmush qurmagan",
        "status_married": "💍 Oilali (Turmush qurgan)",
        "status_divorced": "💔 Ajrashgan (Qonuniy)",
        "status_widowed": "🕊️ Beva (Beva qolgan)",

        # Spouse Prompts
        "spouse_section": "💍 <b>Turmush o'rtog'ingiz ma'lumotlari</b>\n\nAQSh qonunlariga ko'ra turmush o'rtog'i ma'lumotlari va surati kiritilishi majburiy.",
        "spouse_fullname": "Turmush o'rtog'ingizning F.I.SH (Familiya, Ism, Sharifini lotin harflarida kiriting):\n(Masalan: <code>Valiyeva Nigora Rustam qizi</code>):",
        "spouse_gender": "Turmush o'rtog'ingizning jinsini tanlang:",
        "spouse_birth_date": "Turmush o'rtog'ingizning tug'ilgan sanasini kiriting:\nFormat: <code>KK.OO.YYYY</code> (Masalan: <code>20.08.1997</code>):",
        "spouse_birth_place": "Turmush o'rtog'ingizning tug'ilgan joyi (Mamlakat, shahar/tuman):\n(Masalan: <code>O'zbekiston, Buxoro viloyati</code>):",
        "spouse_education": "Turmush o'rtog'ingizning ta'lim darajasini tanlang:",
        "spouse_photo": "📸 <b>Turmush o'rtog'ingizning 5x5 fotosuratini yuboring:</b>\n(Oq fonda, ko'zoynaksiz):",

        # Children Prompts
        "prompt_children_count": "<b>12-qadam:</b> 21 yoshgacha bo'lgan, turmush qurmagan farzandlaringiz sonini tanlang:\n<i>(Agar farzandingiz bo'lmasa, 0 ni bosing)</i>",
        "child_section": "👶 <b>{index}-farzandingiz ma'lumotlari:</b>",
        "child_fullname": "{index}-farzandingizning F.I.SH (Lotin harflarida):\n(Masalan: <code>Valiyev Temur Alisher o'g'li</code>):",
        "child_gender": "{index}-farzandingizning jinsini tanlang:",
        "child_birth_date": "{index}-farzandingizning tug'ilgan sanasini kiriting (KK.OO.YYYY):",
        "child_birth_place": "{index}-farzandingizning tug'ilgan joyi (Mamlakat, shahar):",
        "child_photo": "📸 <b>{index}-farzandingizning 5x5 fotosuratini yuboring:</b>",

        # Review & Submission
        "review_title": "📋 <b>Arizangizni ko'rib chiqing va tasdiqlang</b>\n\nIltimos, kiritilgan barcha ma'lumotlar to'g'riligini sinchiklab tekshiring:\n",
        "review_main_applicant": "👤 <b>Asosiy Arizachi:</b>\n• F.I.SH: <b>{last_name} {first_name} {patronymic}</b>\n• Jinsi: <b>{gender}</b>\n• Tug'ilgan sana: <b>{birth_date}</b>\n• Tug'ilgan joyi: <b>{birth_place}</b>\n• Ta'lim: <b>{education}</b>\n• Manzil: <b>{address}</b>\n• Telefon: <b>{phone}</b>\n• Oilaviy holati: <b>{marital_status}</b>\n",
        "review_spouse": "\n💍 <b>Turmush o'rtog'i:</b>\n• F.I.SH: <b>{fullname}</b>\n• Jinsi: <b>{gender}</b>\n• Tug'ilgan sana: <b>{birth_date}</b>\n• Tug'ilgan joyi: <b>{birth_place}</b>\n• Ta'lim: <b>{education}</b>\n",
        "review_children_header": "\n👶 <b>Farzandlar ({count} ta):</b>\n",
        "review_child_item": "{index}. <b>{fullname}</b> ({gender}, {birth_date}, {birth_place})\n",
        "btn_confirm": "✅ Barchasi to'g'ri, yuborish",
        "btn_restart": "🔄 Qayta to'ldirish",

        # Success message
        "success_submission": (
            "🎉 <b>Arizangiz muvaffaqiyatli qabul qilindi!</b>\n\n"
            "🆔 Sizning arizangiz kodi: <code>{app_code}</code>\n"
            "👤 Ariza egasi: <b>{full_name}</b>\n"
            "📅 Ariza qabul qilingan vaqt: <b>{created_at}</b>\n\n"
            "📄 <i>Arizangizning rasmiy PDF hujjati tayyorlandi va quyida biriktirildi. Uni yuklab olib saqlab qo'yishingiz mumkin.</i>\n\n"
            "💵 <b>To'lov ma'lumotlari:</b>\n"
            "Tarif: <b>{tariff_name} ({tariff_price})</b>\n"
            "To'lov uchun karta: <code>{card_number}</code>\n"
            "Karta egasi: <b>{card_holder}</b>\n\n"
            "<i>Iltimos, to'lovni amalga oshirgach to'lov chekini skrinshot qilib ushbu botga yuboring.</i>\n\n"
            "📢 Rasmiy kanalimizga a'zo bo'ling: {channel}"
        ),
        "cancelled": "❌ Anketa to'ldirish bekor qilindi. Bosh menyudasiz.",

        # Confirmation & Approval Messages
        "msg_payment_approved": (
            "🎉 <b>To'lovingiz tasdiqlandi!</b>\n\n"
            "🆔 Ariza Kodi: <code>{app_code}</code>\n"
            "Arizangiz mutaxassislarimiz tomonidan AQSh Davlat Departamenti rasmiy tizimiga kiritilmoqda.\n"
            "Tez orada rasmiy tasdiq kodi (Confirmation Number) sizga yuboriladi!"
        ),
        "msg_confirmation_issued": (
            "🇺🇸 <b>TABRIKLAYMIZ! ARIZANGIZ RASMIY RO'YXATDAN O'TDI!</b>\n\n"
            "🆔 Ariza Kodi: <code>{app_code}</code>\n"
            "📜 <b>Tasdiq Kodi (Confirmation Number):</b>\n"
            "👉 <code>{conf_number}</code> 👈\n\n"
            "⚠️ <b>DIQQAT:</b> Ushbu kodni skrinshot qilib yoki biror joyga yozib saqlab qo'ying! "
            "May oyida natijalar chiqqanida aynan shu kod orqali natijangizni tekshirishingiz mumkin bo'ladi."
        ),
        "msg_application_rejected": (
            "⚠️ <b>Arizangiz bo'yicha muhim eslatma!</b>\n\n"
            "🆔 Ariza Kodi: <code>{app_code}</code>\n"
            "❌ <b>Sabab:</b> {reason}\n\n"
            "Iltimos, kamchilikni bartaraf etish uchun yangitdan to'ldiring yoki adminimizga murojaat qiling."
        ),

        # Reminder
        "reminder_unpaid": (
            "⏰ <b>Eslatma: Green Card DV-2027 arizangiz kutilmoqda!</b>\n\n"
            "Hurmatli <b>{name}</b>, sizning <code>{app_code}</code> kodli arizangiz qabul qilingan, "
            "ammo to'lov cheki hali qabul qilinmadi.\n\n"
            "AQSh Green Card dasturida o'rinlar va vaqt chegaralangan. Arizangiz rasmiy tizimga muvaffaqiyatli topshirilishi uchun "
            "to'lov chekini skrinshot qilib shu yerga yuborishingizni so'raymiz.\n\n"
            "💳 Karta: <code>{card_number}</code> ({card_holder})"
        ),
    },
    
    "ru": {
        # Start & Language
        "choose_language": "🇷🇺 <b>Здравствуйте!</b>\nДобро пожаловать в официальный бот регистрации Green Card DV-2027.\n\nПожалуйста, выберите язык:\n\n---\n\n🇺🇿 <b>Assalomu alaykum!</b>\nIltimos, tilingizni tanlang:",
        "lang_selected": "✅ Выбран русский язык!",
        "lang_changed": "✅ Язык успешно изменен!",

        # Main Menu Buttons
        "btn_anketa": "📝 Заполнить анкету",
        "btn_website": "🌐 Заполнить на сайте",
        "btn_photo_rules": "📸 Требования к фото",
        "btn_pricing": "💰 Тарифы и оплата",
        "btn_faq": "❓ Частые вопросы (FAQ)",
        "btn_my_status": "🔍 Статус заявки",
        "btn_referral": "👥 Пригласить друзей",
        "btn_change_lang": "🌐 Сменить язык",
        "btn_cancel": "❌ Отмена",
        "btn_skip_patronymic": "❌ Нет отчества (Пропустить)",
        "btn_send_contact": "📱 Отправить номер телефона",

        # Main Menu Welcome
        "main_menu": (
            "🏛 <b>Программа Green Card DV-2027 (США)</b>\n\n"
            "Выберите нужный раздел из меню ниже:\n\n"
            "• 📝 <b>Заполнить анкету</b> — Пошаговое оформление заявки через бот.\n"
            "• 🌐 <b>Заполнить на сайте</b> — Оформление через наше веб-приложение.\n"
            "• 🔍 <b>Статус заявки</b> — Проверка состояния и номер подтверждения.\n"
            "• 👥 <b>Пригласить друзей</b> — Скидка 20,000 сум за каждого друга!\n"
            "• 📸 <b>Требования к фото</b> — Полная инструкция по фото 5х5 см.\n"
            "• 💰 <b>Тарифы и оплата</b> — Стоимость услуг и реквизиты.\n"
            "• ❓ <b>Частые вопросы</b> — Важные правила и нюансы участия."
        ),

        # Status Checker
        "status_empty": "ℹ️ <b>У вас пока нет поданных анкет.</b>\nЧтобы подать заявку, нажмите кнопку 📝 <b>Заполнить анкету</b>.",
        "status_title": "📋 <b>Статус ваших заявок:</b>\n\n",
        "status_item": (
            "🆔 <b>Код анкеты:</b> <code>{app_code}</code>\n"
            "👤 <b>Заявитель:</b> {name}\n"
            "📌 <b>Статус:</b> {status_badge}\n"
            "📅 <b>Дата:</b> {created_at}\n"
            "{details}\n"
            "━━━━━━━━━━━━━━━━━━\n"
        ),
        "badge_submitted": "⏳ <b>На проверке / Ожидает оплаты</b>",
        "badge_paid": "💳 <b>Оплата принята / Вносится в систему США</b>",
        "badge_approved": "✅ <b>ОФИЦИАЛЬНО ЗАРЕГИСТРИРОВАНО!</b>",
        "badge_rejected": "❌ <b>Требуется повторное заполнение</b>",

        # Referral System
        "referral_info": (
            "👥 <b>Приглашайте друзей и получайте скидки!</b>\n\n"
            "Ваша персональная реферальная ссылка:\n"
            "👉 <code>{ref_link}</code>\n\n"
            "💡 <b>Условия:</b>\n"
            "За каждого друга, перешедшего по вашей ссылке и подавшего анкету, вы получаете скидку <b>20,000 сум</b>!\n\n"
            "📊 <b>Ваша статистика:</b>\n"
            "• Приглашено друзей: <b>{invited}</b>\n"
            "• Подали анкету: <b>{applied}</b>\n"
            "• Ваша общая скидка: <b>{discount:,} сум</b>"
        ),

        # Photo Requirements
        "photo_rules": (
            "📸 <b>Требования к фотографии на Green Card (DV-2027)</b>\n\n"
            "Фотография должна на 100% соответствовать строгим критериям Государственного Департамента США:\n\n"
            "1. <b>Размер и формат:</b> 600x600 пикселей (5х5 см), квадратная.\n"
            "2. <b>Фон:</b> Строго белый или светло-серый, ровный, без теней, предметов и узоров.\n"
            "3. <b>Положение лица:</b> По центру, взгляд прямо в камеру, нейтральное выражение (без улыбки, глаза открыты).\n"
            "4. <b>Очки и головные уборы:</b> В очках фотографироваться СТРОГО ЗАПРЕЩЕНО! В платке (по религиозным причинам) лицо должно быть полностью открыто от лба до подбородка.\n"
            "5. <b>Свежесть фото:</b> Фотография должна быть сделана в течение последних 6 месяцев.\n"
            "6. <b>Качество:</b> Запрещен Photoshop, фильтры, ретушь или использование искусственного интеллекта.\n\n"
            "<i>💡 Рекомендуется отправлять фото файлом (Документом), чтобы Telegram не сжимал качество.</i>"
        ),

        # Pricing & Payment
        "pricing": (
            "💰 <b>Тарифы и Способы Оплаты</b>\n\n"
            "Мы гарантируем безошибочное заполнение вашей анкеты, проверку фото на соответствие стандартам США и выдачу официального номера подтверждения (Confirmation Number).\n\n"
            "💵 <b>Тарифы:</b>\n"
            "• 👤 <b>Одиночная анкета (1 человек):</b> 99,000 сум\n"
            "• 👨‍👩‍👧‍👦 <b>Семейная анкета (Супруги + дети):</b> 149,000 сум\n\n"
            "💳 <b>Реквизиты для оплаты (Click / Payme):</b>\n"
            "Номер карты: <code>{card_number}</code>\n"
            "Получатель: <b>{card_holder}</b>\n"
            "Телефон: <b>{phone}</b>\n\n"
            "<i>⚠️ Чек об оплате вы сможете прикрепить после отправки анкеты.</i>"
        ),

        # FAQ
        "faq": (
            "❓ <b>Часто задаваемые вопросы (FAQ)</b>\n\n"
            "<b>1. Что дает Green Card?</b>\n"
            "Право на постоянное проживание, официальную работу, бесплатное школьное образование для детей и получение гражданства США через 5 лет.\n\n"
            "<b>2. Кто может участвовать?</b>\n"
            "Граждане, имеющие законченное среднее образование (11 классов) или диплом колледжа/лицея.\n\n"
            "<b>3. Нужно ли знать английский язык?</b>\n"
            "Нет, для подачи заявки знание языка не требуется.\n\n"
            "<b>4. Нужен ли загранпаспорт?</b>\n"
            "Вы можете заполнить анкету по ID-карте или действующему загранпаспорту.\n\n"
            "<b>5. Когда будут известны результаты?</b>\n"
            "Официальные результаты будут объявлены в начале мая на государственном сайте США."
        ),

        # Anketa FSM Prompts
        "anketa_start": "📝 <b>Заполнение анкеты Green Card DV-2027</b>\n\nПожалуйста, вводите все данные <b>латинскими буквами</b> строго как в вашем паспорте или ID-карте.\n\nВы можете прервать процесс в любой момент нажав '❌ Отмена'.\n\n<b>Шаг 1:</b> Введите вашу Фамилию (Например: <code>Valiyev</code> или <code>Karimova</code>):",
        "prompt_firstname": "<b>Шаг 2:</b> Введите ваше Имя (Например: <code>Alisher</code> или <code>Madina</code>):",
        "prompt_patronymic": "<b>Шаг 3:</b> Введите Отчество латиницей (Например: <code>Rustamovich</code>).\nЕсли отчества нет в паспорте, нажмите кнопку ниже:",
        "prompt_gender": "<b>Шаг 4:</b> Выберите ваш пол:",
        "btn_male": "👨 Мужской",
        "btn_female": "👩 Женский",
        "prompt_birth_date": "<b>Шаг 5:</b> Введите дату вашего рождения.\nФормат: <code>ДД.ММ.ГГГГ</code> (Например: <code>15.04.1995</code>):",
        "error_birth_date": "⚠️ <b>Неверный формат даты!</b>\nПожалуйста, введите дату в формате <code>ДД.ММ.ГГГГ</code> (Например: <code>24.11.1998</code>):",
        "prompt_birth_place": "<b>Шаг 6:</b> Введите страну и город/район вашего рождения:\n(Например: <code>Uzbekistan, Tashkent</code>):",
        "prompt_education": "<b>Шаг 7:</b> Выберите ваш уровень образования:",
        "edu_primary": "🏫 Средняя школа (11 классов)",
        "edu_college": "🎓 Колледж / Лицей / Техникум",
        "edu_bachelor": "🏛 Высшее (Бакалавриат)",
        "edu_master": "📚 Магистратура / Ученая степень",
        "prompt_address": "<b>Шаг 8:</b> Введите ваш фактический адрес проживания:\n(Например: <code>Tashkent, Chilanzar 9, d. 12, kv. 45</code>):",
        "prompt_phone": "<b>Шаг 9:</b> Отправьте ваш номер телефона:\nНажмите кнопку ниже или введите в формате <code>+998901234567</code>:",
        "error_phone": "⚠️ <b>Неверный формат телефона!</b>\nНажмите '📱 Отправить номер' или введите корректный номер (Например: <code>+998901234567</code>):",
        "prompt_photo": "<b>Шаг 10:</b> 📸 <b>Отправьте фотографию главного заявителя.</b>\n\n• Размер 5х5 см (600х600 px), белый фон.\n• Без очков!\n• Желательно файлом (Документом) без сжатия или качественным фото:",
        "error_photo": "⚠️ Пожалуйста, отправьте только изображение или файл фото (JPG/PNG/JPEG)!",
        "prompt_marital_status": "<b>Шаг 11:</b> Выберите ваше семейное положение:",
        "status_single": "👤 Холост / Не замужем",
        "status_married": "💍 Женат / Замужем",
        "status_divorced": "💔 В разводе (Официально)",
        "status_widowed": "🕊️ Вдовец / Вдова",

        # Spouse Prompts
        "spouse_section": "💍 <b>Данные супруга / супруги</b>\n\nПо правилам программы, информация и фото супруга(и) обязательны к заполнению.",
        "spouse_fullname": "Введите Ф.И.О супруга(и) латинскими буквами:\n(Например: <code>Valiyeva Nigora Rustam qizi</code>):",
        "spouse_gender": "Выберите пол супруга(и):",
        "spouse_birth_date": "Введите дату рождения супруга(и):\nФормат: <code>ДД.ММ.ГГГГ</code> (Например: <code>20.08.1997</code>):",
        "spouse_birth_place": "Место рождения супруга(и) (Страна, город):\n(Например: <code>Uzbekistan, Bukhara</code>):",
        "spouse_education": "Уровень образования супруга(и):",
        "spouse_photo": "📸 <b>Отправьте фото супруга(и) 5х5 см:</b>\n(Белый фон, без очков):",

        # Children Prompts
        "prompt_children_count": "<b>Шаг 12:</b> Выберите количество детей до 21 года, не состоящих в браке:\n<i>(Если детей нет, нажмите 0)</i>",
        "child_section": "👶 <b>Данные {index}-го ребенка:</b>",
        "child_fullname": "Ф.И.О {index}-го ребенка (Латиницей):\n(Например: <code>Valiyev Temur Alisher o'g'li</code>):",
        "child_gender": "Выберите пол ребенка:",
        "child_birth_date": "Дата рождения ребенка (ДД.ММ.ГГГГ):",
        "child_birth_place": "Место рождения ребенка (Страна, город):",
        "child_photo": "📸 <b>Отправьте фото {index}-го ребенка 5х5 см:</b>",

        # Review & Submission
        "review_title": "📋 <b>Проверьте и подтвердите ваши данные</b>\n\nПожалуйста, внимательно сверьте все пункты:\n",
        "review_main_applicant": "👤 <b>Основной заявитель:</b>\n• Ф.И.О: <b>{last_name} {first_name} {patronymic}</b>\n• Пол: <b>{gender}</b>\n• Дата рождения: <b>{birth_date}</b>\n• Место рождения: <b>{birth_place}</b>\n• Образование: <b>{education}</b>\n• Адрес: <b>{address}</b>\n• Телефон: <b>{phone}</b>\n• Семейное положение: <b>{marital_status}</b>\n",
        "review_spouse": "\n💍 <b>Супруг(а):</b>\n• Ф.И.О: <b>{fullname}</b>\n• Пол: <b>{gender}</b>\n• Дата рождения: <b>{birth_date}</b>\n• Место рождения: <b>{birth_place}</b>\n• Образование: <b>{education}</b>\n",
        "review_children_header": "\n👶 <b>Дети ({count}):</b>\n",
        "review_child_item": "{index}. <b>{fullname}</b> ({gender}, {birth_date}, {birth_place})\n",
        "btn_confirm": "✅ Все верно, отправить",
        "btn_restart": "🔄 Заполнить заново",

        # Success message
        "success_submission": (
            "🎉 <b>Ваша анкета успешно принята!</b>\n\n"
            "🆔 Код вашей анкеты: <code>{app_code}</code>\n"
            "👤 Заявитель: <b>{full_name}</b>\n"
            "📅 Дата приема: <b>{created_at}</b>\n\n"
            "📄 <i>Официальный PDF документ вашей заявки сформирован и прикреплен ниже.</i>\n\n"
            "💵 <b>Информация об оплате:</b>\n"
            "Тариф: <b>{tariff_name} ({tariff_price})</b>\n"
            "Карта для оплаты: <code>{card_number}</code>\n"
            "Получатель: <b>{card_holder}</b>\n\n"
            "<i>Пожалуйста, после оплаты отправьте чек (скриншот) в этот бот.</i>\n\n"
            "📢 Подпишитесь на наш официальный канал: {channel}"
        ),
        "cancelled": "❌ Заполнение анкеты отменено. Вы в главном меню.",

        # Confirmation & Approval Messages
        "msg_payment_approved": (
            "🎉 <b>Ваша оплата успешно подтверждена!</b>\n\n"
            "🆔 Код анкеты: <code>{app_code}</code>\n"
            "Наши специалисты вносят ваши данные в официальную государственную систему США.\n"
            "В ближайшее время вам будет выдан официальный номер подтверждения (Confirmation Number)!"
        ),
        "msg_confirmation_issued": (
            "🇺🇸 <b>ПОЗДРАВЛЯЕМ! ВАША АНКЕТА ОФИЦИАЛЬНО ЗАРЕГИСТРИРОВАНА!</b>\n\n"
            "🆔 Код анкеты: <code>{app_code}</code>\n"
            "📜 <b>Официальный номер подтверждения (Confirmation Number):</b>\n"
            "👉 <code>{conf_number}</code> 👈\n\n"
            "⚠️ <b>ВНИМАНИЕ:</b> Сделайте скриншот и сохраните этот номер! "
            "Именно по нему в мае проверяются результаты розыгрыша на государственном сайте США."
        ),
        "msg_application_rejected": (
            "⚠️ <b>Важное уведомление по вашей анкете!</b>\n\n"
            "🆔 Код анкеты: <code>{app_code}</code>\n"
            "❌ <b>Причина:</b> {reason}\n\n"
            "Пожалуйста, исправьте указанные замечания или обратитесь к администратору."
        ),

        # Reminder
        "reminder_unpaid": (
            "⏰ <b>Напоминание: Ваша анкета Green Card DV-2027 ждет оплаты!</b>\n\n"
            "Уважаемый(ая) <b>{name}</b>, ваша анкета с кодом <code>{app_code}</code> принята, "
            "но оплата еще не поступила.\n\n"
            "Сроки регистрации ограничены. Чтобы гарантированно успеть подать заявку, "
            "пожалуйста, совершите оплату и отправьте скриншот чека в этот чат.\n\n"
            "💳 Карта: <code>{card_number}</code> ({card_holder})"
        ),
    }
}


def get_text(lang: str, key: str, **kwargs) -> str:
    """Til va kalit bo'yicha matnni olish"""
    current_lang = lang if lang in TEXTS else "uz"
    text_template = TEXTS.get(current_lang, {}).get(key, TEXTS["uz"].get(key, f"[{key}]"))
    if kwargs:
        try:
            return text_template.format(**kwargs)
        except Exception:
            return text_template
    return text_template
