
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


# منوی اصلی کارگاه ها
def workshops_menu():

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(
        KeyboardButton("🖼 بوتکمپ پردازش تصویر کاربردی")
    )

    keyboard.row(
        KeyboardButton("🔙 منوی اصلی")
    )

    return keyboard


# منوی اختصاصی بوتکمپ
def workshop_registration_menu():

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(
        KeyboardButton("📝 ثبت‌نام")
    )

    keyboard.row(
        KeyboardButton("🔙 بازگشت به فهرست دوره‌ها")
    )

    return keyboard


# منوی انصراف
def workshop_cancel_menu():

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(
        KeyboardButton("❌ انصراف")
    )

    return keyboard


# منوی دریافت شماره تماس
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


# منوی انتخاب دانشگاه
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
