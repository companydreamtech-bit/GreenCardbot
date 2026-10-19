import aiosqlite
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from config import config

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_path: str = config.DB_PATH):
        self.db_path = db_path

    async def init_db(self):
        """Ma'lumotlar bazasi jadvallarini yaratish va yangi ustunlarni tekshirish"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    full_name TEXT,
                    language TEXT DEFAULT 'uz',
                    referrer_id INTEGER DEFAULT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    application_code TEXT UNIQUE NOT NULL,
                    user_id INTEGER NOT NULL,
                    status TEXT DEFAULT 'submitted',
                    full_data_json TEXT NOT NULL,
                    confirmation_number TEXT DEFAULT NULL,
                    rejection_reason TEXT DEFAULT NULL,
                    reminder_sent INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
                """
            )

            # Migratsiya: agar jadval avval yaratilgan bo'lsa yangi ustunlarni qo'shish
            try:
                await db.execute("ALTER TABLE users ADD COLUMN referrer_id INTEGER DEFAULT NULL")
            except Exception:
                pass

            try:
                await db.execute("ALTER TABLE applications ADD COLUMN confirmation_number TEXT DEFAULT NULL")
            except Exception:
                pass

            try:
                await db.execute("ALTER TABLE applications ADD COLUMN rejection_reason TEXT DEFAULT NULL")
            except Exception:
                pass

            try:
                await db.execute("ALTER TABLE applications ADD COLUMN reminder_sent INTEGER DEFAULT 0")
            except Exception:
                pass

            await db.commit()
            logger.info("Database initialized with updated schema successfully.")

    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Foydalanuvchi ma'lumotlarini olish"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            )
            row = await cursor.fetchone()
            if row:
                return dict(row)
            return None

    async def add_or_update_user(
        self, user_id: int, username: Optional[str], full_name: str, language: str = "uz", referrer_id: Optional[int] = None
    ):
        """Foydalanuvchini qo'shish yoki yangilash"""
        async with aiosqlite.connect(self.db_path) as db:
            # Agar mavjud bo'lsa referrer_id ni o'chirmaslik
            existing = await self.get_user(user_id)
            if existing:
                await db.execute(
                    """
                    UPDATE users SET
                        username = ?,
                        full_name = ?,
                        language = COALESCE(?, language),
                        updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                    """,
                    (username, full_name, language, user_id),
                )
            else:
                await db.execute(
                    """
                    INSERT INTO users (user_id, username, full_name, language, referrer_id, updated_at)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    """,
                    (user_id, username, full_name, language, referrer_id),
                )
            await db.commit()

    async def set_user_language(self, user_id: int, language: str):
        """Foydalanuvchi tilini o'zgartirish"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET language = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?",
                (language, user_id),
            )
            await db.commit()

    async def get_user_language(self, user_id: int) -> str:
        """Foydalanuvchi tilini olish (default: uz)"""
        user = await self.get_user(user_id)
        if user and user.get("language"):
            return user["language"]
        return "uz"

    async def save_application(
        self, application_code: str, user_id: int, full_data: dict, status: str = "submitted"
    ) -> int:
        """Yangi arizani saqlash"""
        data_json = json.dumps(full_data, ensure_ascii=False)
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """
                INSERT INTO applications (application_code, user_id, status, full_data_json)
                VALUES (?, ?, ?, ?)
                """,
                (application_code, user_id, status, data_json),
            )
            await db.commit()
            return cursor.lastrowid

    async def update_application_status(
        self, application_code: str, status: str, confirmation_number: str = None, rejection_reason: str = None
    ) -> bool:
        """Ariza holatini yangilash (paid, approved, rejected)"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                UPDATE applications SET
                    status = ?,
                    confirmation_number = COALESCE(?, confirmation_number),
                    rejection_reason = COALESCE(?, rejection_reason),
                    updated_at = CURRENT_TIMESTAMP
                WHERE application_code = ?
                """,
                (status, confirmation_number, rejection_reason, application_code),
            )
            await db.commit()
            return True

    async def get_application_by_code(self, application_code: str) -> Optional[Dict[str, Any]]:
        """Arizani kodi bo'yicha olish"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM applications WHERE application_code = ?", (application_code,)
            )
            row = await cursor.fetchone()
            if row:
                res = dict(row)
                res["full_data"] = json.loads(res["full_data_json"])
                return res
            return None

    async def get_user_applications(self, user_id: int) -> List[Dict[str, Any]]:
        """Foydalanuvchining barcha arizalarini olish"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM applications WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,),
            )
            rows = await cursor.fetchall()
            applications = []
            for row in rows:
                item = dict(row)
                item["full_data"] = json.loads(item["full_data_json"])
                applications.append(item)
            return applications

    async def get_unpaid_applications_for_reminder(self) -> List[Dict[str, Any]]:
        """To'lov qilinmagan va eslatma yuborilmagan arizalarni olish (masalan, 3 soatdan oshgan)"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """
                SELECT a.*, u.language, u.full_name as user_name
                FROM applications a
                JOIN users u ON a.user_id = u.user_id
                WHERE a.status = 'submitted' AND a.reminder_sent = 0
                AND datetime(a.created_at, '+3 hours') <= datetime('now')
                """
            )
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

    async def mark_reminder_sent(self, application_code: str):
        """Eslatma yuborilganini belgilash"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE applications SET reminder_sent = 1 WHERE application_code = ?",
                (application_code,),
            )
            await db.commit()

    async def get_referral_stats(self, user_id: int) -> Dict[str, Any]:
        """Foydalanuvchining referal statistikasi"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT COUNT(*) FROM users WHERE referrer_id = ?", (user_id,)
            )
            invited_count = (await cursor.fetchone())[0]

            # Taklif qilinganlardan nechtasi ariza topshirgan
            cursor = await db.execute(
                """
                SELECT COUNT(DISTINCT a.user_id)
                FROM applications a
                JOIN users u ON a.user_id = u.user_id
                WHERE u.referrer_id = ?
                """,
                (user_id,),
            )
            applied_count = (await cursor.fetchone())[0]

            return {
                "invited_count": invited_count,
                "applied_count": applied_count,
                "discount_sum": applied_count * 20000,  # Har bir topshirgan do'st uchun 20,000 so'm chegirma
            }

    async def get_all_users(self, lang: Optional[str] = None) -> List[Dict[str, Any]]:
        """Rassilka (Broadcast) uchun barcha foydalanuvchilar ro'yxati"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            if lang:
                cursor = await db.execute("SELECT * FROM users WHERE language = ?", (lang,))
            else:
                cursor = await db.execute("SELECT * FROM users")
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

    async def count_stats(self) -> Dict[str, int]:
        """Admin uchun statistika"""
        async with aiosqlite.connect(self.db_path) as db:
            users_cur = await db.execute("SELECT COUNT(*) FROM users")
            users_count = (await users_cur.fetchone())[0]

            apps_cur = await db.execute("SELECT COUNT(*) FROM applications")
            apps_count = (await apps_cur.fetchone())[0]

            paid_cur = await db.execute("SELECT COUNT(*) FROM applications WHERE status = 'paid'")
            paid_count = (await paid_cur.fetchone())[0]

            appr_cur = await db.execute("SELECT COUNT(*) FROM applications WHERE status = 'approved'")
            approved_count = (await appr_cur.fetchone())[0]

            return {
                "users_count": users_count,
                "applications_count": apps_count,
                "paid_count": paid_count,
                "approved_count": approved_count,
            }


db = Database()
