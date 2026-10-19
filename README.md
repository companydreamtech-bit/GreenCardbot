# 🇺🇸 Green Card DV-2027 Telegram Boti

AQSh Green Card DV-2027 dasturiga arizalarni qabul qiluvchi, ikki tilli (O‘zbek va Rus), to‘liq avtomatlashtirilgan professional Telegram Bot.

- **Veb-sayt:** [https://greencard-dv2027.vercel.app](https://greencard-dv2027.vercel.app)
- **Telegram Kanal:** [@greencarddv_2027](https://t.me/greencarddv_2027)
- **Admin Guruh ID:** `-1004332225482`

---

## 🌟 Asosiy Xususiyatlari

1. **Ikki tilli tizim (O'zbekcha / Русский):** Foydalanuvchi tilni erkin tanlaydi va barcha bosqichlar tanlangan tilda olib boriladi.
2. **Telegram Web App integratsiyasi:** Bot ichida rasmiy veb-saytni to'g'ridan-to'g'ri ochish imkoniyati.
3. **Bosqichma-bosqich FSM Anketa:**
   - Asosiy arizachi ma'lumotlari (F.I.SH, jinsi, tug'ilgan sana va joyi, ta'limi, yashash manzili, telefon raqami).
   - Fotosurat talablari bo'yicha yo'riqnoma va rasmni sifatini saqlagan holda qabul qilish.
   - Oilaviy holati (agar oilali bo'lsa, turmush o'rtog'ining to'liq ma'lumotlari va 5x5 fotosurati).
   - 21 yoshgacha bo'lgan bolalar soni va har bir farzand uchun alohida ma'lumotlar va fotosuratlar.
4. **Ko'rib chiqish (Review) bosqichi:** Foydalanuvchi yuborishdan oldin barcha ma'lumotlarni tekshirishi yoki qayta to'ldirishi mumkin.
5. **Admin Guruhga To'liq Integratsiya:**
   - `DV2027-UZ-XXXXXX` unikal kod generatsiya qilinadi.
   - Admin guruhiga to'liq HTML hisobot yuboriladi.
   - Arizachi bilan bog'lanish uchun inline tugmalar (`💬 Telegram orqali yozish` va `📞 Tel orqali Telegram ochish`).
   - Barcha fotosuratlar asl sifatda alohida hujjat (`sendDocument`) ko'rinishida jo'natiladi.
6. **SQLite Arxivlash:** Barcha foydalanuvchilar va arizalar `greencard.db` bazasida asinxron saqlanadi.

---

## 📂 Loyiha Strukturasi

```
GreenCardbot/
├── config.py                 # Bot konfiguratsiyasi (.env orqali)
├── main.py                   # Botni ishga tushirish (Dispatcher, Polling)
├── requirements.txt          # Python kutubxonalari
├── .env                      # Muhit o'zgaruvchilari (Token, Admin ID)
├── .env.example              # Namuna konfiguratsiya
├── .gitignore
├── database/
│   ├── __init__.py
│   └── db.py                 # SQLite asinxron (aiosqlite) boshqaruvi
├── handlers/
│   ├── __init__.py           # Barcha routerlarni birlashtirish
│   ├── start.py              # /start va til tanlash
│   ├── info.py               # Qoidalar, tariflar, to'lov, FAQ, bekor qilish
│   ├── anketa.py             # Bosqichma-bosqich FSM ariza to'ldirish
│   └── admin.py              # Admin buyruqlari (/stats, /check)
├── keyboards/
│   ├── __init__.py
│   ├── default.py            # Asosiy menyu (Web App), kontakt yuborish
│   └── inline.py             # Til, jins, ta'lim, oila, review, admin tugmalari
├── locales/
│   ├── __init__.py
│   └── texts.py              # Ikki tilli (UZ / RU) matnlar lug'ati
├── states/
│   ├── __init__.py
│   └── anketa.py             # Aiogram FSM holatlari (AnketaStates)
└── utils/
    ├── __init__.py
    ├── helpers.py            # Unikal kod yaratish va HTML hisobot
    └── validators.py         # Sana va telefon raqam validatsiyasi
```

---

## 🚀 O'rnatish va Ishga Tushirish

### 1. Virtual muhit yaratish va faollashtirish:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / MacOS
python3 -m venv venv
source venv/bin/activate
```

### 2. Kutubxonalarni o'rnatish:
```bash
pip install -r requirements.txt
```

### 3. Konfiguratsiyani sozlash (.env):
`.env` faylini oching va bot tokeningizni kiriting:
```ini
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_GROUP_ID=-1004332225482
ADMIN_IDS=123456789
WEB_APP_URL=https://greencard-dv2027.vercel.app
CHANNEL_USERNAME=@greencarddv_2027
PAYMENT_CARD_NUMBER=8600 0000 0000 0000
PAYMENT_CARD_HOLDER=GREEN CARD ADMIN
PAYMENT_PHONE=+998901234567
DB_PATH=greencard.db
```

### 4. Botni ishga tushirish:
```bash
python main.py
```

---

## 🛠 Admin Buyruqlari
- `/stats` — Umumiy foydalanuvchilar va yuborilgan arizalar soni.
- `/check <kod>` — Masalan: `/check DV2027-UZ-738491` ariza ma'lumotlarini qidirish.
