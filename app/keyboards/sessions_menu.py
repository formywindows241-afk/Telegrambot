from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def session_details_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton("📝 ثبت‌نام"))
    keyboard.row(KeyboardButton("🔙 بازگشت به رویدادهای فعال"))
    return keyboard


def session_cancel_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton("❌ انصراف"))
    return keyboard


def session_phone_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        KeyboardButton("📱 ارسال شماره تلفن", request_contact=True)
    )
    keyboard.row(KeyboardButton("❌ انصراف"))
    return keyboard


def session_degree_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(KeyboardButton("کاردانی"))
    keyboard.row(KeyboardButton("کارشناسی"))
    keyboard.row(KeyboardButton("کارشناسی ارشد"))
    keyboard.row(KeyboardButton("دکترا"))
    keyboard.row(KeyboardButton("❌ انصراف"))

    return keyboard


def session_entry_year_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(
        KeyboardButton("ورودی 401 یا پایین‌تر"),
        KeyboardButton("ورودی 402"),
    )
    keyboard.row(
        KeyboardButton("ورودی 403"),
        KeyboardButton("ورودی 404"),
    )
    keyboard.row(KeyboardButton("❌ انصراف"))

    return keyboard


def session_university_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(KeyboardButton("دانشگاه یزد"))
    keyboard.row(KeyboardButton("دانشگاه میبد"))
    keyboard.row(KeyboardButton("دانشگاه علم و هنر"))
    keyboard.row(KeyboardButton("سایر"))
    keyboard.row(KeyboardButton("❌ انصراف"))

    return keyboard