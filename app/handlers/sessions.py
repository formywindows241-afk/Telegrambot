
from pathlib import Path

from telebot import TeleBot

from app.config import ADMIN_ID
from app.keyboards.main_menu import main_menu
from app.keyboards.events_menu import active_events_menu
from app.keyboards.sessions_menu import (
    session_details_menu,
    session_cancel_menu,
    session_phone_menu,
    session_degree_menu,
    session_entry_year_menu,
    session_university_menu,
)


SESSIONS = {'fourth_session': {'title': '💻 سیری در جهان کامپیوتر | فصل دوم، جلسه چهارم',
                    'text': '🟢 مسیر ورود به فناوری\u200cهای پیشرفته و فرصت\u200cهای شغلی این حوزه '
                            'چطور شکل می\u200cگیره؟ آیا برای فعالیت در این زمینه\u200cها باید به '
                            'سیلیکون\u200cولی رفت؟\n'
                            '\n'
                            '🔵 در چهارمین جلسه از فصل دوم مجموعه\u200cنشست\u200cهای «سیری در جهان '
                            'کامپیوتر»، گفت\u200cوگویی متفاوت با حضور دو مهمان از دنیای دانشگاه و '
                            'صنعت خواهیم داشت.\n'
                            '\n'
                            '🟢 در این نشست درباره تأثیر هوش مصنوعی بر آینده مهندسی کامپیوتر، مسیر '
                            'ورود به بازار کار، تجربه\u200cهای دانشگاهی و صنعتی و چگونگی ایجاد '
                            'تعادل میان یادگیری دانشگاهی و کسب تجربه عملی گفت\u200cوگو '
                            'می\u200cکنیم.\n'
                            '\n'
                            '🎙️ میزبان دکتر علی\u200cمحمد لطیف، عضو هیئت علمی دانشگاه یزد، و مهندس '
                            'حمیدرضا جعفریان\u200cمقدم، مدیرعامل شرکت رایانش ابری آوید هستیم تا '
                            'این موضوعات را از نگاه دانشگاه و صنعت بررسی کنیم.\n'
                            '\n'
                            '📅 پنجشنبه، ۱۲ آذر ۱۴۰۵\n'
                            '⏰ ساعت ۹ تا ۱۱\n'
                            '📍 دانشگاه یزد، دانشکده منابع طبیعی، سالن منتظر قائم\n'
                            '💰 شرکت در نشست رایگان است.',
                    'poster': 'session_four.jpg',
                    'registration_open': True,
                    'report_url': None}}



ASSETS_PATH = Path(__file__).resolve().parents[1] / "assets"


DEGREES = [
    "کاردانی",
    "کارشناسی",
    "کارشناسی ارشد",
    "دکترا",
]

ENTRY_YEARS = [
    "ورودی 401 یا پایین‌تر",
    "ورودی 402",
    "ورودی 403",
    "ورودی 404",
]

UNIVERSITIES = [
    "دانشگاه یزد",
    "دانشگاه میبد",
    "دانشگاه علم و هنر",
    "سایر",
]


# متن سؤال پایانی ثبت‌نام
# برای تغییر سؤال، فقط همین مقدار را ویرایش کنید.
FINAL_QUESTION = "مهمترین دغدغه یا اولویت شما برای شروع مسیر شغلی و رشد حرفه ای چیست ؟"


selected_sessions = {}
registration_data = {}


def register_sessions_handler(bot: TeleBot):

    # نمایش اطلاعات نشست انتخاب‌شده
    @bot.message_handler(
        func=lambda message: (
            message.text is not None
            and message.text.strip() in {
                session["title"]
                for session in SESSIONS.values()
            }
        )
    )
    def show_session_details(message):
        user_id = message.from_user.id
        selected_title = message.text.strip()

        session_id = next(
            (
                key
                for key, session in SESSIONS.items()
                if session["title"] == selected_title
            ),
            None,
        )

        print(f"[SESSIONS] selected_title={selected_title!r}")
        print(f"[SESSIONS] selected_session_id={session_id!r}")

        if session_id is None:
            bot.send_message(
                message.chat.id,
                "❌ نشست موردنظر پیدا نشد.",
                reply_markup=active_events_menu(),
            )
            return

        selected_sessions[user_id] = session_id
        session = SESSIONS[session_id]

        poster_path = ASSETS_PATH / session["poster"]

        print(f"[SESSIONS] poster_path={poster_path}")
        print(f"[SESSIONS] poster_exists={poster_path.is_file()}")

        # ارسال پوستر و متن در یک پیام
        if poster_path.is_file():
            try:
                with poster_path.open("rb") as poster:
                    bot.send_photo(
                        message.chat.id,
                        poster,
                        caption=(
                            f"{session['title']}\n\n"
                            f"{session['text']}"
                        ),
                        reply_markup=session_details_menu(),
                    )

            except Exception as error:
                print(f"[SESSIONS] photo_send_error: {error}")

                bot.send_message(
                    message.chat.id,
                    f"{session['title']}\n\n{session['text']}",
                    reply_markup=session_details_menu(),
                )

        else:
            bot.send_message(
                message.chat.id,
                f"{session['title']}\n\n{session['text']}",
                reply_markup=session_details_menu(),
            )

    # بازگشت از جزئیات نشست به فهرست رویدادهای فعال
    @bot.message_handler(
        func=lambda message: (
            message.text is not None
            and message.text.strip() == "🔙 بازگشت به رویدادهای فعال"
        )
    )
    def back_to_active_events(message):
        user_id = message.from_user.id
        selected_sessions.pop(user_id, None)
        registration_data.pop(user_id, None)

        bot.send_message(
            message.chat.id,
            "🟢 رویدادهای فعال انجمن\\n\\n"
            "لطفاً رویداد موردنظر خود را انتخاب کنید:",
            reply_markup=active_events_menu(),
        )

    # شروع ثبت‌نام
    @bot.message_handler(
        func=lambda message: (
            message.text is not None
            and message.text.strip() == "📝 ثبت‌نام"
        )
    )
    def start_registration(message):
        user_id = message.from_user.id
        session_id = selected_sessions.get(user_id)

        if session_id not in SESSIONS:
            bot.send_message(
                message.chat.id,
                "لطفاً ابتدا یک نشست را انتخاب کنید.",
                reply_markup=main_menu(),
            )
            return

        session = SESSIONS[session_id]

        # بررسی وضعیت ثبت‌نام
        if not session["registration_open"]:
            report_url = session.get("report_url")

            if report_url:
                bot.send_message(
                    message.chat.id,
                    (
                        'این رویداد قبلاً برگزار شده و از '
                        f'<a href="{report_url}">'
                        'اینجا</a> می‌تونی گزارش تصویریشو ببینی 😉'
                    ),
                    parse_mode="HTML",
                    reply_markup=session_details_menu(),
                )
            else:
                bot.send_message(
                    message.chat.id,
                    "ثبت‌نام این نشست بسته شده است.",
                    reply_markup=session_details_menu(),
                )

            return

        registration_data[user_id] = {
            "session_id": session_id
        }

        bot.send_message(
            message.chat.id,
            "لطفاً نام و نام خانوادگی خود را وارد کنید:",
            reply_markup=session_cancel_menu(),
        )

        bot.register_next_step_handler(
            message,
            get_name,
            session_id,
        )

    # دریافت نام
    def get_name(message, session_id):
        user_id = message.from_user.id

        if is_cancel(message):
            return

        if not message.text or not message.text.strip():
            bot.send_message(
                message.chat.id,
                "لطفاً نام و نام خانوادگی خود را وارد کنید.",
                reply_markup=session_cancel_menu(),
            )
            bot.register_next_step_handler(
                message, get_name, session_id
            )
            return

        registration_data[user_id]["name"] = message.text.strip()

        bot.send_message(
            message.chat.id,
            "لطفاً شماره تلفن خود را با دکمه زیر ارسال کنید:",
            reply_markup=session_phone_menu(),
        )

        bot.register_next_step_handler(
            message,
            get_phone,
            session_id,
        )

    # دریافت شماره تلفن
    def get_phone(message, session_id):
        user_id = message.from_user.id

        if is_cancel(message):
            return

        if not message.contact:
            bot.send_message(
                message.chat.id,
                "لطفاً از دکمه ارسال شماره تلفن استفاده کنید.",
                reply_markup=session_phone_menu(),
            )
            bot.register_next_step_handler(
                message, get_phone, session_id
            )
            return

        if (
            message.contact.user_id is not None
            and message.contact.user_id != user_id
        ):
            bot.send_message(
                message.chat.id,
                "لطفاً شماره تلفن خودتان را ارسال کنید.",
                reply_markup=session_phone_menu(),
            )
            bot.register_next_step_handler(
                message, get_phone, session_id
            )
            return

        registration_data[user_id]["phone"] = (
            message.contact.phone_number
        )

        bot.send_message(
            message.chat.id,
            "لطفاً مقطع تحصیلی خود را انتخاب کنید:",
            reply_markup=session_degree_menu(),
        )

        bot.register_next_step_handler(
            message,
            get_degree,
            session_id,
        )

    # دریافت مقطع تحصیلی
    def get_degree(message, session_id):
        user_id = message.from_user.id

        if is_cancel(message):
            return

        degree = message.text.strip() if message.text else ""

        if degree not in DEGREES:
            bot.send_message(
                message.chat.id,
                "لطفاً مقطع تحصیلی را از گزینه‌ها انتخاب کنید.",
                reply_markup=session_degree_menu(),
            )
            bot.register_next_step_handler(
                message, get_degree, session_id
            )
            return

        registration_data[user_id]["degree"] = degree

        bot.send_message(
            message.chat.id,
            "لطفاً سال ورودی خود را انتخاب کنید:",
            reply_markup=session_entry_year_menu(),
        )

        bot.register_next_step_handler(
            message,
            get_entry_year,
            session_id,
        )

    # دریافت سال ورودی
    def get_entry_year(message, session_id):
        user_id = message.from_user.id

        if is_cancel(message):
            return

        entry_year = message.text.strip() if message.text else ""

        if entry_year not in ENTRY_YEARS:
            bot.send_message(
                message.chat.id,
                "لطفاً سال ورودی را از گزینه‌ها انتخاب کنید.",
                reply_markup=session_entry_year_menu(),
            )
            bot.register_next_step_handler(
                message, get_entry_year, session_id
            )
            return

        registration_data[user_id]["entry_year"] = entry_year

        bot.send_message(
            message.chat.id,
            "دانشگاه خود را انتخاب کنید:",
            reply_markup=session_university_menu(),
        )

        bot.register_next_step_handler(
            message,
            get_university,
            session_id,
        )

    # دریافت دانشگاه
    def get_university(message, session_id):
        user_id = message.from_user.id

        if is_cancel(message):
            return

        university = message.text.strip() if message.text else ""

        if university not in UNIVERSITIES:
            bot.send_message(
                message.chat.id,
                "لطفاً دانشگاه را از گزینه‌ها انتخاب کنید.",
                reply_markup=session_university_menu(),
            )
            bot.register_next_step_handler(
                message, get_university, session_id
            )
            return

        if university == "سایر":
            bot.send_message(
                message.chat.id,
                "لطفاً نام دانشگاه خود را وارد کنید:",
                reply_markup=session_cancel_menu(),
            )
            bot.register_next_step_handler(
                message,
                get_other_university,
                session_id,
            )
            return

        registration_data[user_id]["university"] = university

        ask_final_question(message, session_id)

    # دریافت نام دانشگاه سایر
    def get_other_university(message, session_id):
        user_id = message.from_user.id

        if is_cancel(message):
            return

        if not message.text or not message.text.strip():
            bot.send_message(
                message.chat.id,
                "لطفاً نام دانشگاه خود را وارد کنید.",
                reply_markup=session_cancel_menu(),
            )
            bot.register_next_step_handler(
                message,
                get_other_university,
                session_id,
            )
            return

        registration_data[user_id]["university"] = (
            message.text.strip()
        )

        ask_final_question(message, session_id)

    # دریافت دغدغه کاربر درباره محیط کار
    def ask_final_question(message, session_id):
        bot.send_message(
            message.chat.id,
            FINAL_QUESTION,
            reply_markup=session_cancel_menu(),
        )

        bot.register_next_step_handler(
            message,
            get_final_answer,
            session_id,
        )

    def get_final_answer(message, session_id):
        user_id = message.from_user.id

        if is_cancel(message):
            return

        if not message.text or not message.text.strip():
            bot.send_message(
                message.chat.id,
                "لطفاً پاسخ خود را به‌صورت متنی وارد کنید:",
                reply_markup=session_cancel_menu(),
            )
            bot.register_next_step_handler(
                message,
                get_final_answer,
                session_id,
            )
            return

        registration_data[user_id]["work_concern"] = message.text.strip()

        send_registration_to_admin(message, session_id)

    # ارسال اطلاعات ثبت‌نام به ادمین
    def send_registration_to_admin(message, session_id):
        user_id = message.from_user.id
        user = message.from_user

        data = registration_data.get(user_id)

        if not data:
            bot.send_message(
                message.chat.id,
                "اطلاعات ثبت‌نام پیدا نشد. لطفاً دوباره تلاش کنید.",
                reply_markup=main_menu(),
            )
            return

        session = SESSIONS[session_id]

        username = (
            f"@{user.username}"
            if user.username
            else "ندارد"
        )

        # پیام اول: اطلاعات معمول ثبت‌نام، با همان قالب قبلی
        admin_message = (
            "🎙️ ثبت‌نام جدید در نشست علمی\n\n"
            f"📌 عنوان نشست: {session['title']}\n"
            f"👤 نام و نام خانوادگی: {data['name']}\n"
            f"🔗 نام کاربری: {username}\n"
            f"🆔 شناسه تلگرام: {user.id}\n"
            f"📱 شماره تلفن: {data['phone']}\n"
            f"🎓 مقطع تحصیلی: {data['degree']}\n"
            f"📚 سال ورودی: {data['entry_year']}\n"
            f"🏛 دانشگاه: {data['university']}"
        )

        # پیام دوم: فقط پاسخ سؤال پایانی
        concern_message = (
            "💬 دغدغه شما برای کار:\n\n"
            f"{data['work_concern']}"
        )

        try:
            if not ADMIN_ID:
                raise ValueError("ADMIN_ID تنظیم نشده است.")

            # ارسال پیام اول
            bot.send_message(
                ADMIN_ID,
                admin_message,
            )

            # ارسال پیام دوم
            bot.send_message(
                ADMIN_ID,
                concern_message,
            )

        except Exception as error:
            print(f"[SESSIONS] admin_send_error: {error}")

            bot.send_message(
                message.chat.id,
                "❌ ارسال اطلاعات ثبت‌نام با مشکل مواجه شد. لطفاً بعداً دوباره تلاش کنید.",
                reply_markup=main_menu(),
            )

            registration_data.pop(user_id, None)
            selected_sessions.pop(user_id, None)
            return

        registration_data.pop(user_id, None)
        selected_sessions.pop(user_id, None)

        bot.send_message(
            message.chat.id,
            "✅ ثبت‌نام شما با موفقیت انجام شد.",
            reply_markup=main_menu(),
        )

    # لغو عملیات
    def is_cancel(message):
        if message.text and message.text.strip() == "❌ انصراف":
            user_id = message.from_user.id

            registration_data.pop(user_id, None)
            selected_sessions.pop(user_id, None)

            bot.send_message(
                message.chat.id,
                "ثبت‌نام لغو شد.",
                reply_markup=main_menu(),
            )

            return True

        return False
