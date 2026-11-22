
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def workshops_menu():

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(
        KeyboardButton("🖼 بوتکمپ پردازش تصویر کاربردی")
    )

    keyboard.row(
        KeyboardButton("🔙 منوی اصلی")
    )

    return keyboard


def workshop_registration_menu():

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(
        KeyboardButton("📝 پیش‌ثبت‌نام بوتکمپ")
    )

    keyboard.row(
        KeyboardButton("🔙 بازگشت به فهرست کارگاه‌ها")
    )

    return keyboard


def workshop_cancel_menu():

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(
        KeyboardButton("❌ انصراف")
    )

    return keyboard


def workshop_contact_menu():

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(
        KeyboardButton(
            "📱 ارسال شماره تماس",
            request_contact=True
        )
    )

    keyboard.row(
        KeyboardButton("❌ انصراف")
    )

    return keyboard


def workshop_university_menu():

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(
        KeyboardButton("دانشگاه یزد"),
        KeyboardButton("علم و هنر")
    )

    keyboard.row(
        KeyboardButton("دانشگاه آزاد"),
        KeyboardButton("سایر")
    )

    keyboard.row(
        KeyboardButton("❌ انصراف")
    )

    return keyboard
