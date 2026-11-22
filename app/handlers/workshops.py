
from telebot import TeleBot
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from app.config import ADMIN_ID

from app.keyboards.main_menu import main_menu

from app.keyboards.workshops_menu import (
    workshops_menu,
    workshop_registration_menu,
    workshop_cancel_menu,
    workshop_contact_menu,
    workshop_university_menu
)


def register_workshops_handler(bot: TeleBot):

    # نگهداری اطلاعات موقت ثبت نام کاربران
    user_data = {}

    # =====================================
    # منوی کارگاه ها
    # =====================================

    @bot.message_handler(
        func=lambda message: message.text == "🛠 کارگاه‌ها"
    )
    def workshops(message):

        bot.send_message(
            message.chat.id,
            "🛠 به بخش کارگاه‌ها خوش آمدید.\n\n"
            "لطفاً کارگاه موردنظر خود را انتخاب کنید:",
            reply_markup=workshops_menu()
        )

    # =====================================
    # بازگشت به منوی اصلی
    # =====================================

    @bot.message_handler(
        func=lambda message: message.text == "🔙 منوی اصلی"
    )
    def back_to_main(message):

        user_data.pop(message.from_user.id, None)

        bot.send_message(
            message.chat.id,
            "به منوی اصلی بازگشتید.",
            reply_markup=main_menu()
        )

    # =====================================
    # انتخاب بوتکمپ
    # =====================================

    @bot.message_handler(
        func=lambda message:
        message.text == "🖼 بوتکمپ پردازش تصویر کاربردی"
    )
    def select_bootcamp(message):

        bot.send_message(
            message.chat.id,
            "🖼 بوتکمپ پردازش تصویر کاربردی\n\n"
            "برای شرکت در این بوتکمپ، "
            "دکمه ثبت‌نام را انتخاب کنید.",
            reply_markup=workshop_registration_menu()
        )

    # =====================================
    # بازگشت به فهرست کارگاه ها
    # =====================================

    @bot.message_handler(
        func=lambda message:
        message.text == "🔙 بازگشت به فهرست دوره‌ها"
    )
    def back_to_workshops(message):

        user_data.pop(message.from_user.id, None)

        bot.send_message(
            message.chat.id,
            "لطفاً کارگاه موردنظر خود را انتخاب کنید:",
            reply_markup=workshops_menu()
        )

    # =====================================
    # بررسی انصراف
    # =====================================

    def is_cancelled(message):

        if message.text == "❌ انصراف":

            user_data.pop(message.from_user.id, None)

            bot.send_message(
                message.chat.id,
                "درخواست ثبت‌نام شما لغو شد.",
                reply_markup=main_menu()
            )

            return True

        return False

    # =====================================
    # شروع ثبت نام
    # =====================================

    @bot.message_handler(
        func=lambda message: message.text == "📝 ثبت‌نام"
    )
    def start_registration(message):

        user_id = message.from_user.id

        user_data[user_id] = {
            "full_name": None,
            "is_student": None,
            "student_id": None,
            "phone": None,
            "university": None
        }

        sent = bot.send_message(
            message.chat.id,
            "📝 ثبت‌نام بوتکمپ پردازش تصویر کاربردی\n\n"
            "لطفاً نام و نام خانوادگی خود را وارد کنید:",
            reply_markup=workshop_cancel_menu()
        )

        bot.register_next_step_handler(
            sent,
            receive_name
        )

    # =====================================
    # دریافت نام و نام خانوادگی
    # =====================================

    def receive_name(message):

        if is_cancelled(message):
            return

        user_id = message.from_user.id

        if user_id not in user_data:
            return

        if not message.text:

            ask_name(message.chat.id)
            return

        full_name = message.text.strip()

        # بررسی کاراکترهای مجاز
        valid_characters = all(
            char.isalpha()
            or char.isspace()
            or char in ["\u200c", "-"]
            for char in full_name
        )

        # بررسی وجود حداقل دو بخش نام
        name_parts = full_name.replace(
            "\u200c", " "
        ).split()

        if not valid_characters or len(name_parts) < 2:

            bot.send_message(
                message.chat.id,
                "❌ نام و نام خانوادگی نامعتبر است.\n\n"
                "لطفاً نام و نام خانوادگی خود را "
                "بدون عدد یا کاراکترهای خاص وارد کنید."
            )

            ask_name(message.chat.id)
            return

        user_data[user_id]["full_name"] = full_name

        ask_student_status(message.chat.id)

    def ask_name(chat_id):

        sent = bot.send_message(
            chat_id,
            "لطفاً نام و نام خانوادگی خود را وارد کنید:",
            reply_markup=workshop_cancel_menu()
        )

        bot.register_next_step_handler(
            sent,
            receive_name
        )

    # =====================================
    # پرسش دانشجو بودن
    # =====================================

    def ask_student_status(chat_id):

        keyboard = InlineKeyboardMarkup()

        keyboard.row(
            InlineKeyboardButton(
                "بله",
                callback_data="workshop_student_yes"
            ),
            InlineKeyboardButton(
                "خیر",
                callback_data="workshop_student_no"
            )
        )

        keyboard.row(
            InlineKeyboardButton(
                "❌ انصراف",
                callback_data="workshop_student_cancel"
            )
        )

        bot.send_message(
            chat_id,
            "🎓 آیا دانشجو هستید؟",
            reply_markup=keyboard
        )

    # =====================================
    # دریافت پاسخ دانشجو بودن
    # =====================================

    @bot.callback_query_handler(
        func=lambda call:
        call.data in [
            "workshop_student_yes",
            "workshop_student_no",
            "workshop_student_cancel"
        ]
    )
    def receive_student_status(call):

        bot.answer_callback_query(call.id)

        user_id = call.from_user.id
        chat_id = call.message.chat.id

        # فقط در گفتگوی خصوصی
        if call.message.chat.type != "private":
            return

        if user_id != chat_id:
            return

        if user_id not in user_data:
            return

        # جلوگیری از پردازش مجدد پاسخ
        if user_data[user_id]["is_student"] is not None:
            return

        # انصراف
        if call.data == "workshop_student_cancel":

            user_data.pop(user_id, None)

            bot.send_message(
                chat_id,
                "درخواست ثبت‌نام شما لغو شد.",
                reply_markup=main_menu()
            )

            return

        # پاسخ بله
        if call.data == "workshop_student_yes":

            user_data[user_id]["is_student"] = True

            sent = bot.send_message(
                chat_id,
                "لطفاً شماره دانشجویی خود را وارد کنید:",
                reply_markup=workshop_cancel_menu()
            )

            bot.register_next_step_handler(
                sent,
                receive_student_id
            )

        # پاسخ خیر
        else:

            user_data[user_id]["is_student"] = False

            ask_phone(chat_id)

    # =====================================
    # دریافت شماره دانشجویی
    # =====================================

    def receive_student_id(message):

        if is_cancelled(message):
            return

        user_id = message.from_user.id

        if user_id not in user_data:
            return

        student_id = (
            message.text.strip()
            if message.text
            else ""
        )

        # فقط عدد و عدم یکسان بودن تمام ارقام
        if (
            not student_id.isdigit()
            or len(set(student_id)) == 1
        ):

            bot.send_message(
                message.chat.id,
                "❌ شماره دانشجویی نامعتبر است.\n\n"
                "شماره باید فقط شامل اعداد باشد "
                "و تمام ارقام آن یکسان نباشند.\n\n"
                "مثال نامعتبر: 00000000 یا 11111111"
            )

            sent = bot.send_message(
                message.chat.id,
                "لطفاً دوباره شماره دانشجویی خود را وارد کنید:",
                reply_markup=workshop_cancel_menu()
            )

            bot.register_next_step_handler(
                sent,
                receive_student_id
            )

            return

        user_data[user_id]["student_id"] = student_id

        ask_phone(message.chat.id)

    # =====================================
    # درخواست شماره تماس
    # =====================================

    def ask_phone(chat_id):

        sent = bot.send_message(
            chat_id,
            "📱 لطفاً شماره تماس خود را با استفاده "
            "از دکمه زیر ارسال کنید:",
            reply_markup=workshop_contact_menu()
        )

        bot.register_next_step_handler(
            sent,
            receive_phone
        )

    # =====================================
    # دریافت شماره تماس
    # =====================================

    def receive_phone(message):

        if is_cancelled(message):
            return

        user_id = message.from_user.id

        if user_id not in user_data:
            return

        contact = message.contact

        if not contact:

            sent = bot.send_message(
                message.chat.id,
                "❌ لطفاً شماره تماس را فقط از طریق "
                "دکمه ارسال شماره تماس بفرستید.",
                reply_markup=workshop_contact_menu()
            )

            bot.register_next_step_handler(
                sent,
                receive_phone
            )

            return

        # بررسی اینکه شماره متعلق به خود کاربر باشد
        if (
            contact.user_id is not None
            and contact.user_id != user_id
        ):

            sent = bot.send_message(
                message.chat.id,
                "❌ لطفاً شماره تماس متعلق به خودتان "
                "را ارسال کنید.",
                reply_markup=workshop_contact_menu()
            )

            bot.register_next_step_handler(
                sent,
                receive_phone
            )

            return

        user_data[user_id]["phone"] = contact.phone_number

        # اگر دانشجو باشد، دانشگاه دریافت می شود
        if user_data[user_id]["is_student"]:

            ask_university(message.chat.id)

        else:

            finish_registration(message)

    # =====================================
    # درخواست انتخاب دانشگاه
    # =====================================

    def ask_university(chat_id):

        sent = bot.send_message(
            chat_id,
            "🎓 لطفاً دانشگاه محل تحصیل خود را انتخاب کنید:",
            reply_markup=workshop_university_menu()
        )

        bot.register_next_step_handler(
            sent,
            receive_university
        )

    # =====================================
    # دریافت دانشگاه
    # =====================================

    def receive_university(message):

        if is_cancelled(message):
            return

        user_id = message.from_user.id

        if user_id not in user_data:
            return

        university = message.text

        valid_universities = [
            "دانشگاه یزد",
            "علم و هنر",
            "دانشگاه آزاد",
            "سایر"
        ]

        if university not in valid_universities:

            sent = bot.send_message(
                message.chat.id,
                "❌ لطفاً یکی از گزینه‌های موجود را انتخاب کنید:",
                reply_markup=workshop_university_menu()
            )

            bot.register_next_step_handler(
                sent,
                receive_university
            )

            return

        # اگر سایر انتخاب شد
        if university == "سایر":

            sent = bot.send_message(
                message.chat.id,
                "لطفاً نام دانشگاه خود را وارد کنید:",
                reply_markup=workshop_cancel_menu()
            )

            bot.register_next_step_handler(
                sent,
                receive_other_university
            )

            return

        user_data[user_id]["university"] = university

        finish_registration(message)

    # =====================================
    # دریافت نام سایر دانشگاه ها
    # =====================================

    def receive_other_university(message):

        if is_cancelled(message):
            return

        user_id = message.from_user.id

        if user_id not in user_data:
            return

        if not message.text or not message.text.strip():

            sent = bot.send_message(
                message.chat.id,
                "لطفاً نام دانشگاه خود را وارد کنید:",
                reply_markup=workshop_cancel_menu()
            )

            bot.register_next_step_handler(
                sent,
                receive_other_university
            )

            return

        user_data[user_id]["university"] = (
            message.text.strip()
        )

        finish_registration(message)

    # =====================================
    # تکمیل و ارسال ثبت نام
    # =====================================

    def finish_registration(message):

        user_id = message.from_user.id

        data = user_data.get(user_id)

        if not data:
            return

        user = message.from_user

        username = (
            f"@{user.username}"
            if user.username
            else "ندارد"
        )

        student_status = (
            "بله"
            if data["is_student"]
            else "خیر"
        )

        admin_message = (
            "📝 ثبت‌نام جدید بوتکمپ پردازش تصویر کاربردی\n\n"

            f"👤 نام و نام خانوادگی: "
            f"{data['full_name']}\n"

            f"🎓 دانشجو: {student_status}\n"

            f"🆔 شماره دانشجویی: "
            f"{data['student_id'] or 'ندارد'}\n"

            f"📱 شماره تماس: {data['phone']}\n"

            f"🏛 دانشگاه: "
            f"{data['university'] or 'ندارد'}\n\n"

            f"🔗 Username: {username}\n"

            f"🆔 Telegram ID: {user.id}"
        )

        try:

            bot.send_message(
                ADMIN_ID,
                admin_message
            )

        except Exception:

            bot.send_message(
                message.chat.id,
                "❌ متأسفانه هنگام ارسال اطلاعات "
                "مشکلی پیش آمد.\n"
                "لطفاً کمی بعد دوباره تلاش کنید.",
                reply_markup=main_menu()
            )

            user_data.pop(user_id, None)

            return

        # حذف اطلاعات موقت
        user_data.pop(user_id, None)

        bot.send_message(
            message.chat.id,
            "🎉 ثبت‌نام شما با موفقیت انجام شد!\n\n"
            "اطلاعات شما برای مسئول ثبت‌نام ارسال شد.\n\n"
            "از حضور شما در بوتکمپ پردازش تصویر کاربردی "
            "سپاسگزاریم.",
            reply_markup=main_menu()
        )
